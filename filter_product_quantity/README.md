Filter Numberic value on product.
==================================

By default, OpenERP won't allow user to filter products based on their
'Onhand Quantity' or 'Virtual Quantity'.

This module will overcome this limitation, support both search and sorting
on those field.

默认情况下，OpenERP不允许用户根据产品的'在手数量'或'未来数量'来过滤产品

本模块突破了该种限制，同时支持对这些字段的搜索和排序。

Note:
Sorting on function field feature in this module will work directly For OpenERP V6.x.
As OpenERP V7.x removed the sorting function field in 'web addon', to make sorting works
will need to modify slightly on 'web' module.

TODO: will develop a module to generalize the 'sorting on function field' feature

注意：OpenERP V6.x安装本模块后，可直接对产品列表中的Onhand Quantity, Virtual Quantity 等函数字段的排序
因为V7中在'web addon'中禁止了对函数字段的排序操作，需要对'web'模块做少量修改来完成排序

TODO: 将开发模块实现通用的为函数字段排序的功能(不仅仅是对本模块所支持的产品列表字段）
