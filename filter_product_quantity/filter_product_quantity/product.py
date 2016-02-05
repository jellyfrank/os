# -*- coding: utf-8 -*-
##############################################################################
#
#    Filter on Stock quantity - OpenERP Module
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

from openerp.osv import fields, osv
import decimal_precision as dp
from openerp.addons.stock.product import product_product as spp
from openerp.addons.product.product import product_product as pp

_product_available = spp._product_available
_product_lst_price = pp._product_lst_price

SORTABLE_FUNC_FIELD = ('qty_available', 'virtual_available', 'lst_price')

def condition(operand, left, right):
    if operand == '=':
        operand = '=='
    return eval(' '.join((str(left),operand,str(right))))

class product_product(osv.osv):
    _inherit = "product.product"

    def _search_fnct(self, cr, uid, args, qty_type, context=None):
        context = context or {}
        print 'context', context
        ids = self.search(cr, uid, [], context=context)
        qty_products = self.read(cr, uid, ids, [qty_type], context=context)
        res = []
        for q in qty_products:
            if condition(args[0][1], q[qty_type], args[0][2]): 
                res.append(q['id'])
        return [('id', 'in', res)]
    
    def _search_qty_available(self, cr, uid, obj, name, args, context):
        return self._search_fnct(cr, uid, args, 'qty_available', context)

    def _search_virtual_available(self, cr, uid, obj, name, args, context):
        return self._search_fnct(cr, uid, args, 'virtual_available', context)

    def _search_lst_price(self, cr, uid, obj, name, args, context):
        return self._search_fnct(cr, uid, args, 'lst_price', context)
            
    _columns = {
        'qty_available': fields.function(_product_available,
            multi='qty_available', type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            fnct_search=_search_qty_available,
            string='Quantity On Hand',
            help="Current quantity of products.\n"
                 "In a context with a single Stock Location, this includes "
                 "goods stored at this Location, or any of its children.\n"
                 "In a context with a single Warehouse, this includes "
                 "goods stored in the Stock Location of this Warehouse, or any"
                 "of its children.\n"
                 "In a context with a single Shop, this includes goods "
                 "stored in the Stock Location of the Warehouse of this Shop, "
                 "or any of its children.\n"
                 "Otherwise, this includes goods stored in any Stock Location "
                 "with 'internal' type."),
        'virtual_available': fields.function(_product_available,
            multi='qty_available', type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            fnct_search=_search_virtual_available,
            string='Forecasted Quantity',
            help="Forecast quantity (computed as Quantity On Hand "
                 "- Outgoing + Incoming)\n"
                 "In a context with a single Stock Location, this includes "
                 "goods stored in this location, or any of its children.\n"
                 "In a context with a single Warehouse, this includes "
                 "goods stored in the Stock Location of this Warehouse, or any"
                 "of its children.\n"
                 "In a context with a single Shop, this includes goods "
                 "stored in the Stock Location of the Warehouse of this Shop, "
                 "or any of its children.\n"
                 "Otherwise, this includes goods stored in any Stock Location "
                 "with 'internal' type."),
        'lst_price' : fields.function(_product_lst_price, type='float',
            string='Public Price', fnct_search=_search_lst_price,
            digits_compute=dp.get_precision('Product Price')),
        }

    def search(self, cr, uid, args, offset=0, limit=None, order=None,
            context=None, count=False):
        context = context or {}
        func_flds = []
        if order:
            order_part = order.split(',')[0]
            order_split = order_part.strip().split(' ')
            order_field = order_split[0].strip()
            order_direction = order_split[1].strip() if len(order_split) == 2 else ''
            if order_field in SORTABLE_FUNC_FIELD:
                    func_flds.append((order_field, order_direction))
        ids = super(product_product, self).search(cr, uid, args, offset, limit,
                order, context, count)
        if func_flds:
            for fld, order in func_flds:
                val = self.read(cr, uid, ids, [fld], context=context)
                sorted_val = sorted(val, key=lambda x: x[fld],
                        reverse=(order=='DESC'))
            ids = map(lambda x: x['id'], sorted_val)
        return ids

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
