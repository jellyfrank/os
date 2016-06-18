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

from openerp.addons.web.http import Controller, route, request
from openerp.addons.web.controllers.main import _serialize_exception
from openerp.osv import osv
from openerp.tools import html_escape

import simplejson
from werkzeug import exceptions, url_decode
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
from werkzeug.datastructures import Headers
from reportlab.graphics.barcode import createBarcodeDrawing
from openerp.addons.report.controllers.main import ReportController
import openerp


class QunarPDFController(ReportController):

	@route(['/report/download'], type='http', auth="user")
	def report_download(self, data, token):
		"""This function is used by 'qwebactionmanager.js' in order to trigger the download of
		 a pdf/controller report.

		:param data: a javascript array JSON.stringified containg report internal url ([0]) and
		type [1]
		:returns: Response with a filetoken cookie and an attachment header
		"""
		requestcontent = simplejson.loads(data)
		url, type = requestcontent[0], requestcontent[1]
		try:
			if type == 'qweb-pdf':
				reportname = url.split('/report/pdf/')[1].split('?')[0]

				docids,filename = None,None
				if '/' in reportname:
					reportname, docids = reportname.split('/')
				if docids:
				    # Generic report:				    
					response = self.report_routes(reportname, docids=docids, converter='pdf')
					#Rename the pdf's name make it looks kindly.
					report_ids = request.registry.get('ir.actions.report.xml').search(request.cr,openerp.SUPERUSER_ID,[('report_name','=',reportname)])
					if len(report_ids):
						report_obj = request.registry.get('ir.actions.report.xml').browse(request.cr,openerp.SUPERUSER_ID,report_ids[0])
						docids = [int(x) for x in docids.split(',')]
						reports = request.registry.get(report_obj.model).browse(request.cr,openerp.SUPERUSER_ID,docids)
						filename = reports[0].name
				else:
				    # Particular report:
					data = url_decode(url.split('?')[1]).items()  # decoding the args represented in JSON
					response = self.report_routes(reportname, converter='pdf', **dict(data))				
				
				response.headers.add('Content-Disposition', 'attachment; filename=%s.pdf;' % (filename or reportname))
				response.set_cookie('fileToken', token)
				return response
			elif type =='controller':
				reqheaders = Headers(request.httprequest.headers)
				response = Client(request.httprequest.app, BaseResponse).get(url, headers=reqheaders, follow_redirects=True)
				response.set_cookie('fileToken', token)
				return response
			else:
				return
		except Exception, e:
			se = _serialize_exception(e)
			error = {
			    'code': 200,
			    'message': "Odoo Server Error",
			    'data': se
			}
			return request.make_response(html_escape(simplejson.dumps(error)))