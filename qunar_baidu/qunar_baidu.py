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

from openerp import api,_,models,fields
import werkzeug

def urlplus(url, params):
    return werkzeug.Href(url)(params or None)

class res_partner(models.Model):
	_inherit="res.partner"

	@api.model
	def baidu_map_img(self,zoom=14, width=298, height=298):
		params = {
			'center':(self.city and self.city.name or '')+(self.street or ''),
			'size':"%sx%s" % (height, width),
			'zoom': zoom,
		}
		print params
		return urlplus('//api.map.baidu.com/staticimage', params)

	@api.model 
	def baidu_map_link(self,zoom=10):
		params={
			'address':(self.country_id and self.country_id.name or '')+(self.city and self.city.name or '')+(self.street or ''),
			'output':'html',
		}
		return urlplus('http://api.map.baidu.com/geocoder',params)

class res_company(models.Model):
	_inherit='res.company'

	@api.model
	def baidu_map_img(self,zoom=18, width=298, height=298):
		return self.partner_id and self.partner_id.baidu_map_img(zoom=zoom,width=width,height=height) or None

	@api.model 
	def baidu_map_link(self,zoom=10):
		return self.partner_id and self.partner_id.baidu_map_link(zoom=zoom) or None

