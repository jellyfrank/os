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

{
	'name':"Stock Report",
	"author":"KevinKong(742829100@qq.com),碎石头(360026606@qq.com),广州救火(7017511@qq.com)",
	"version":"10.0.2.0",
	'depends':['stock'],
	"description":
u"""
进销存报表
===========================
* 进销存报表

模块说明
---------------------------
本模块为去哪儿网版本的修改版(odoo8.0)，删除了一些依赖模块，重新划分为独立的进销存报表模块
现已开源，助力Odoo中国社区的发展。
如果有好的建议和疑问，欢迎电邮 kfx2007@163.com 或 QQ群：56721527。
由碎石头(360026606@qq.com),广州救火(7017511@qq.com)将模块升级支持odoo10.0

""",
	"category":"stock",
	"installable":True,
	'application':True,
	"data":[
		"security/ir.model.access.csv",
		"qunar_report_stock_view.xml"
		],
}