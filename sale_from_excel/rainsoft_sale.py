# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Qingdao Rainsoft (<kfx2007@163.com>)
#    Author:Kevin Kong
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

from openerp.osv import osv,fields
from openerp.tools.translate import _
from tempfile import TemporaryFile
import openerp.addons.decimal_precision as dp
import xlrd,base64
import logging

_logger = logging.getLogger(__name__)

class rainsoft_sale(osv.osv):
	_name="sale.order"
	_inherit="sale.order"
	

	_columns={
			'data':fields.binary('File'),
		}
	
	
	def import_file(self,cr,uid,ids,context=None):
			for wiz in self.browse(cr,uid,ids):
					if not wiz.data:continue
			excel = xlrd.open_workbook(file_contents=base64.decodestring(wiz.data))
			sheets = excel.sheets()
			for sh in sheets:
					if sh.name:
							lines=[]
							for row in range(1,sh.nrows):
									if sh.cell(row,1).value and sh.cell(row,5).value:
											product_no = int(str(sh.cell(row,1).value).strip().split('.')[0])
											product_amount=sh.cell(row,5).value
											product_price =sh.cell(row,6).value
											product_method=sh.cell(row,12).value
											if product_method == u'订单':
													product_method='make_to_order'
											else:
													product_method='make_to_stock'
				    
											products = self.pool.get('product.product').search(cr,uid,[('default_code','=',product_no)],context=context)
											_logger.info("importing product_no:"+str(product_no)+";products:"+str(products))
											if len(products)>0 and product_amount>0 and product_amount:
													product = self.pool.get('product.product').browse(cr,uid,products[0],context=context)
													line={
															'order_id':ids[0],
															'name':product.name,
															'product_id':product.id,
															'price_unit':product_price,
															'product_uom':product.uom_id.id,
															'product_uom_qty':product_amount,
												'type':product_method,
												'state':'draft',
															}
													self.pool.get('sale.order.line').create(cr,uid,line,context)
											else:
													_logger.info("product insert failed. No:"+str(product_no))
													_logger.info("probably caused by 1.len(products):"+str(len(products))+",2.product_amount:"+str(product_amount))
									else:
											_logger.info('row 1 and row 5 is invalid! Error Column 1:'+str(sh.cell(row,1).value)+";Error Column 2:"+str(sh.cell(row,5).value))
				    
	
		

rainsoft_sale()

