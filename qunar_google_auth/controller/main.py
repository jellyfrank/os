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

import logging
import werkzeug
import openerp
import urllib2
import json

from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.web.controllers.main import ensure_db,login_and_redirect

import pyotp

class google(openerp.addons.web.controllers.main.Home):

	@http.route('/web/login',type='http',auth='public',website=True)
	def web_login(self,*args,**kargs):
		if request.httprequest.method=='POST' and not request.params.get('qsso'):
			#Check Google Authentication
			uids = request.registry.get('res.users').search(request.cr,openerp.SUPERUSER_ID,[('login','=',request.params['login'])])
			qcontext={}
			if not len(uids):
				qcontext['error'] =  _("User doesn't exist! Please contact system administrator!")
			user = request.registry.get('res.users').browse(request.cr,openerp.SUPERUSER_ID,uids)
			
			if user.enable_google_auth and user.otp_str:
				totp = pyotp.TOTP(user.otp_str)
				otpcode = totp.now()
				check_code = request.params['password'][-6:]
				check_passwd = request.params['password'][:-6]
				if request.params['password'][-6:] == otpcode:
					request.params['password']=check_passwd
					return super(google,self).web_login(*args,**kargs)
				else:
					qcontext['error'] = 'Your Google Authentication Failed!'
					return request.render('web.login', qcontext)
		return super(google,self).web_login(*args,**kargs)