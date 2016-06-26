# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp.addons.web import http
from openerp.addons.web.http import request
from PIL import Image
import json,os

class main(http.Controller):

	@http.route('/filemanager',type='http',auth="public",website=True,csrf=False)
	def _store_file(self,*args,**kwargs):
		print '*******'
		img = kwargs['imgFile']
		path = os.path.abspath(os.path.realpath(__file__)).split('controller')[0]+'static/files'
		#os.path.abspath(join(os.getcwd(),'/web_kindeditor/static/files'))
		filepath = path+'/'+img.filename
		img.save(filepath)
		url = request.env['ir.config_parameter'].get_param('web.base.url')+"/web_kindeditor/static/files/"+img.filename
		print url
		return json.dumps({'error':0,'url':url})
