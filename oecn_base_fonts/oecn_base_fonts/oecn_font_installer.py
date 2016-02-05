# -*- coding: utf-8 -*-
#__author__ = jeff@openerp.cn, joshua@openerp.cn
##############################################################################
#
#    pdf report support for your language - OpenERP Module
#    Copyright (C) 2013 Shine IT (<http://www.openerp.cn>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from reportlab.lib.fontfinder import FontFinder
import openerp.report.render.rml2pdf.customfonts as cfonts
from reportlab.lib.styles import ParagraphStyle
from reportlab import rl_config
import simplejson as json
import re

try:
    from openerp import SUPERUSER_ID
except ImportError:
    SUPERUSER_ID = SUPERUSER_ID
    
#patch for ReportLab
import reportlab_patch

RMLS = ['rml_header', 'rml_header2', 'rml_header3']
OE_FONTS = ['Helvetica', 'DejaVuSans', 'Times', 'Times-Roman', 'Courier']


class oecn_base_fonts_map(osv.osv_memory):
    _name = 'oecn_base_fonts.map'
    _description = 'The line base fonts mapping'

    # try to get the font from the cache first (system_fonts)
    system_fonts = []
    
    def get_system_fonts(self, cr, uid, context=None):
        if self.system_fonts:
            return self.system_fonts
        else:
            return self._system_fonts_get(cr, uid)
        
    def _system_fonts_get(self, cr, uid, context=None):
        ''' get fonts list on server '''
        # consider both windows and unix like systems
        # get all folders under fonts/ directory
        res = []
        ff = FontFinder(useCache=False)
        fontdirs = []
        if not context:
            context = {}
        fontdirs += rl_config.TTFSearchPath[:] + \
            rl_config.T1SearchPath[:] + \
            rl_config.CMapSearchPath[:]
        ff.addDirectories(set(fontdirs))
        ff.search()
        for familyName in ff.getFamilyNames():
            for font in ff.getFontsInFamily(familyName):
                if font.fileName[-4:].lower() in (".ttf", ".ttc"):
                    try:
                        fileName = font.fileName.decode('utf-8')
                    except UnicodeDecodeError:
                        #for Chinese file name(Windows OS)
                        fileName = font.fileName.decode('gbk')
                    res.append((fileName, font.name))

        #cache the font list in class variable
        oecn_base_fonts_map.system_fonts = res
        return res

    def _pdf_fonts_get(self, cr, uid, context=None):
        return [('Helvetica', 'Helvetica'),
                ('DejaVuSans', 'DejaVuSans'),
                ('Times', 'Times'),
                ('Times-Roman', 'Times-Roman'),
                ('Courier', 'Courier')]

    _columns = {
        'pdf_font': fields.selection(_pdf_fonts_get, 'Original Fonts', 
                                     required=True),
        'new_font': fields.selection(get_system_fonts, 'Replaced With', 
                                     required=True),
        'name': fields.char('Font Alias', size=20, required=True, 
                            help='use this font alias in custom rml report \
                            template'),        
    }
    
    def onchange_new_font(self, cr, uid, ids, new_font):
        """get the default 'Font Alias'"""

        for font_path, font_name in self.system_fonts:
            if new_font == font_path:
                return {'value': {'name': font_name}}
            
oecn_base_fonts_map()


class oecn_font_installer(osv.osv_memory):
    _name = 'oecn.font.installer'
    _inherit = 'res.config.installer'
    
    def _convert_system_font_2_base_font(self, wrap_style, new_mappings):
        if not new_mappings:
            return False
        new_mappings = json.loads(new_mappings)
        cfonts.CustomTTFonts = new_mappings
        if wrap_style:
            ParagraphStyle.defaults['wordWrap'] = 'CJK'
        return True
                    
    def __init__(self, pool, cr):
        super(osv.osv_memory, self).__init__(pool, cr)
        config_obj = pool.get("ir.config_parameter")
        wrap_style = config_obj.get_param(cr, SUPERUSER_ID, 'wrap_style')
        new_mappings = config_obj.get_param(cr, SUPERUSER_ID, 'fonts_map')
        self._convert_system_font_2_base_font(wrap_style, new_mappings)
        
    _columns = {
        'wrap': fields.boolean('CJK wrap', required=True, 
                               help="If you are using CJK fonts, \
                               check this option will wrap your \
                               words properly at the edge of the  pdf report"),
        'map_ids': fields.many2many('oecn_base_fonts.map', 
                                    'oecn_base_font_conf_ref',
                                    'conf_id', 'map_id', 'Replace Fonts'),
        
    }
    
    def _get_wrap(self, cr, uid, *args):
        wrap_style = self.pool.get('ir.config_parameter').get_param(
            cr, SUPERUSER_ID, 'wrap_style')
        return wrap_style

    def _get_map_ids(self, cr, uid, *args):
        mappings = self.pool.get('ir.config_parameter').get_param(
            cr, SUPERUSER_ID, 'fonts_map')

        mappings_obj = self.pool.get('oecn_base_fonts.map')
        default_fonts = None, None
        ids = []
        if mappings:
            mappings = json.loads(mappings)        
            for mapping in mappings:
                val = {'pdf_font': mapping[0],
                       'name': mapping[1],
                       'new_font': mapping[2]}
                try:
                    id = mappings_obj.create(cr, uid, val)
                    ids.append(id)
                except Exception:
                    mappings = None
                    mappings_obj.unlink(cr, uid, ids)
        if not mappings:
            system_fonts = mappings_obj.get_system_fonts(cr, uid)
            for font_path, name, in system_fonts: 
                if name in ('SimHei', 'SimSun', 'WenQuanYiZenHei'):
                    default_fonts = (font_path, name)
                    break
            for fonts in OE_FONTS:
                val = {'pdf_font': fonts,
                       'name': default_fonts[1] or system_fonts[0][1],
                       'new_font': default_fonts[0] or system_fonts[0][0]}
                id = mappings_obj.create(cr, uid, val)
                ids.append(id)                    
        return ids

    _defaults = {
        'wrap': _get_wrap,
        'map_ids': _get_map_ids,
    }
    
    def execute(self, cr, uid, ids, context=None):
        company_obj = self.pool.get('res.company')
        company_ids = company_obj.search(cr, uid, [])
        p1 = re.compile('<setFont name=".*?" ')
        p2 = re.compile('fontName=".*?" ')
        for o in self.browse(cr, uid, ids, context=context):
            config_obj = self.pool.get('ir.config_parameter')
            new_mappings = json.dumps([(new_mapping.pdf_font,
                                        new_mapping.name,
                                        new_mapping.new_font,
                                        'all') 
                                       for new_mapping in o.map_ids])
            config_obj.set_param(cr, uid, 'wrap_style', o.wrap)
            config_obj.set_param(cr, uid, 'fonts_map', new_mappings)
            for company in company_obj.read(cr, uid, company_ids, RMLS):
                '''
                To be improved
                Becacuse some report(header and footer, custom_default.xml, 
                hr_custom_default.xml, hr_custom_default.xml) 
                releady  <setfont='DejaVu sans'/>  in the rml.             
                '''
                value = {}
                for rml in RMLS:
                    new_font_rml = '<setFont name="' + o.map_ids[0].name + '" '
                    value[rml] = p1.sub(new_font_rml, company[rml])
                    value[rml] = p2.sub('fontName="' + o.map_ids[0].name + '" ', value[rml])
                company_obj.write(cr, uid, company['id'], value)            
            self._convert_system_font_2_base_font(o.wrap, new_mappings)
            
        
            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

