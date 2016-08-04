# -*- encoding:utf-8 -*-
# __author__ = jeff@openerp.cn

from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp 

#-------------------------------------------
# Products
#-------------------------------------------
class product_template(osv.osv):
    _inherit = "product.template"
    _columns = {
        'standard_price': fields.float('Cost Price', required=True, \
                          read=['base.group_sale_manager'],                                  
                          digits_compute=dp.get_precision('Purchase Price'), \
                          help="Product's cost for accounting stock valuation. It is the base price for the supplier price."),
    }
product_template()
    
