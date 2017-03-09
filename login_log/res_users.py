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

from openerp import api,fields,_,models,SUPERUSER_ID
from openerp.http import root,request
from openerp.exceptions import except_orm

class res_users(models.Model):
    _inherit="res.users"

    online = fields.Boolean(u'是否在线',compute="_get_online")
    sid = fields.Char('Last Session Id')

    @api.one
    def _get_online(self):
        uids = [root.session_store.get(sid).uid for sid in root.session_store.list() if root.session_store.get(sid).uid]
        if self.id in uids:
            self.online = True
        else:
            self.online = False
    
    def check_credentials(self,cr,uid,password):
        res = super(res_users,self).check_credentials(cr,uid,password)
        user = self.browse(cr,SUPERUSER_ID,uid)
        if user.sid and user.sid!=request.session.sid:
            root.session_store.delete(root.session_store.get(user.sid))
        user.sid = request.session.sid
        return res
    