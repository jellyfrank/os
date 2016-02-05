# -*- coding: utf-8 -*-
# __author__ = tony@openerp.cn,joshua@openerp.cn
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

{
    "name" : "pdf report support for your language",
    "version" : "2.1.1",
    "author" : "Shine IT",
    "maintainer":"jeff@openerp.cn",
    "website": "http://www.openerp.cn",
    "description": u"""
pdf report support for your language
=====================================

Fonts defined in the default report may not support characters
in your language, which may cause jarbled characters in the printed
pdf report.

This addon will solve abovementioned issue elegently by using openerp
customfonts API to replace the original fonts with your seleted fonts.

1) Put your font to your font`s directory (Eg. 'HOME/yourname/fonts')
2) Click the link on the line of 'Configure fonts mapping for pdf report' (Settings/ Configuration/ General Settings/)

You can found your fonts mapping in Settings/Technical/Parameters/System Parameters/fonts_map

More Detail(中文安装指南): http://cn.openerp.cn/openerp_v7_oecn_base_fonts/

by shineit<contact@openerp.cn>""",
    "depends" : ["base",'base_setup'],
    "category" : "Generic Modules/Base",
    "demo_xml" : [],
    "update_xml" : [
        "oecn_font_installer.xml",
        "res_config_view.xml",
        ],
    "license": "GPL-3",
    "active": False,
    "installable": True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

