var Qweb= openerp.web.qweb ;
var _lt = openerp.web._lt;
var _t = openerp.web._t;

openerp.web_graph_radar = openerp.web_graph.Graph.include({
    start: function() {        
        var self = this;
        this.table = $('<table>');
        this.$('.graph_main_content').append(this.table);

        var indexes = {'pivot': 0, 'bar': 1, 'line': 2, 'chart': 3,'radar':4};
        this.$('.graph_mode_selection label').eq(indexes[this.mode]).addClass('active');

        if (this.mode !== 'pivot') {
            this.$('.graph_heatmap label').addClass('disabled');
            this.$('.graph_main_content').addClass('graph_chart_mode');
        } else {
            this.$('.graph_main_content').addClass('graph_pivot_mode');
        }

        // get search view
        var parent = this.getParent();
        while (!(parent instanceof openerp.web.ViewManager)) {
            parent = parent.getParent();
        }
        this.search_view = parent.searchview;

        openerp.session.rpc('/web_graph/check_xlwt').then(function (result) {
            self.$('.graph_options_selection label').last().toggle(result);
        });

        return this.model.call('fields_get', {
                    context: this.graph_view.dataset.context
                }).then(function (f) {
            self.fields = f;
            self.fields.__count = {field:'__count', type: 'integer', string:_t('Count')};
            self.groupby_fields = self.get_groupby_fields();
            self.measure_list = self.get_measures();
            self.add_measures_to_options();
            self.pivot_options.row_groupby = self.create_field_values(self.pivot_options.row_groupby || []);
            self.pivot_options.col_groupby = self.create_field_values(self.pivot_options.col_groupby || []);
            self.pivot_options.measures = self.create_field_values(self.pivot_options.measures || [{field:'__count', type: 'integer', string:'Count'}]);
            self.pivot = new openerp.web_graph.PivotTable(self.model, self.domain, self.fields, self.pivot_options);
            self.pivot.update_data().then(function () {
                self.display_data();
                if (self.graph_view) {
                    self.graph_view.register_groupby(self.pivot.rows.groupby, self.pivot.cols.groupby);
                }
            });
            openerp.web.bus.on('click', self, function (event) {
                if (self.dropdown) {
                    self.$row_clicked = $(event.target).closest('tr');
                    self.dropdown.remove();
                    self.dropdown = null;
                }
            });
            self.put_measure_checkmarks();
        });
    },

    radar:function(){
        var self = this,
            dim_x = this.pivot.rows.groupby.length,
            dim_y = this.pivot.rows.groupby.length;

        var rows = this.pivot.get_rows_with_depth(dim_x),
            labels = _.pluck(rows, 'title');

        var data = _.map(rows,function(row){
                var totals = self.pivot.get_total(row);
                var res = []
                for (m=0;m<self.pivot.measures.length;m++){
                    res.push({'axis':self.pivot.measures[m].string,'value':totals[m]})
                }
                return {'className':row.title,'axes':res};
        }); 

       RadarChart.draw(".graph_main_content div", data);
    },
});