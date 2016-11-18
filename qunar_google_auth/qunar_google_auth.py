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

from openerp import fields,_,api,models
from openerp.exceptions import except_orm
import pyotp,qrcode,StringIO,base64
from openerp import SUPERUSER_ID
import openerp

class res_users(models.Model):
	_inherit='res.users'

	enable_google_auth = fields.Boolean(u'启用Google两步验证')

	otp_str = fields.Char('QR Codes')
	google_auth_img = fields.Binary('Google Authontication QR',compute="_get_qr_img")

	@api.one 
	def btn_gen(self):
		base32 = pyotp.random_base32()
		self.otp_str = base32


	@api.one 
	def _get_qr_img(self):
		#check login 
		if '@' not in self.login:
			raise except_orm(_('Error!'),_('Invlid Login!'))
		totp = pyotp.TOTP(self.otp_str)
		qrcodes = totp.provisioning_uri(self.login)
		img = qrcode.make(qrcodes)
		buf = StringIO.StringIO()
		img.save(buf,'PNG')
		self.google_auth_img = buf.getvalue().encode('base64')
