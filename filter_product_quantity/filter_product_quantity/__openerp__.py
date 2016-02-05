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

{
    'name': 'Filter On Stock Quantity',
    'version': '1.1',
    'author': 'Shine IT',
    'summary': 'Inventory, Logistic, Storage',
    'description' : """
    Filter Numberic value on product.

    By default, OpenERP won't allow user to filter products based on their
    'Onhand Quantity' ,'Virtual Quantity', 'Public Price' etc.

    This module will overcome this limitation, support both search and sorting
    on those field.

    默认情况下，OpenERP不允许用户根据产品的'在手数量'或'未来数量'来过滤产品

    本模块突破了该种限制，同时支持对这些字段的搜索和排序。
    """,
    'website': 'http://www.openerp.cn',
    'depends': ['product', 'stock',],
    'category': 'Warehouse Management',
    'sequence': 16,
    'demo': [
    ],
    'data': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
