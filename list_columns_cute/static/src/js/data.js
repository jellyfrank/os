openerp.list_columns_cute = openerp.web.ListView.include({
	start:function(){
		//console.log(openerp.web.qweb.render('QListView'));
		this._template="QListView";
		return this._super();
	},
});