define(function(require, exports) {
    'use strict';

    var Backbone = require('backbone');

    var PositionView = Backbone.View.extend({
        className: 'position',

        events: {
            'click': 'openProblem'
        },

        render: function() {
            this.$el.html(this.model.get('name'));
            return this;
        },

        openProblem: function() {

        }
    });

    var TeamView = Backbone.View.extend({
        className: 'team',
        render: function() {
            this.$el.html(this.model.get('name') + ' <b>(' + this.model.get('position') + ')</b>');
            return this;
        }
    });

    var Layer = Backbone.View.extend({
        className: 'layer'
    });

    exports.PositionLayer = Layer.extend({

        childView: PositionView,

        initialize: function() {
            this.children = [];
        },

        render: function() {
            this.collection.each(this.addChild, this);
            return this;
        },

        addChild: function(child) {
            var view = new this.childView({model: child});
            this.children.push(view);
            this.$el.append(view.render().$el);
        }

    });

    exports.TeamLayer = exports.PositionLayer.extend({
        childView: TeamView
    });

    exports.MapView = Backbone.View.extend({
        el: '#map',

        initialize: function() {
            this.layers = [];
            this.zIndex = 1;
        },

        render: function() {
            this.$el.empty();
            return this.renderLayers();
        },

        renderLayers: function() {
            var self = this;
            _.each(this.layers, function(layer) {
                self.$el.append(layer.render().$el);
            });
            return this;
        },

        addLayer: function(layer) {
            layer.$el.css('zIndex', this.zIndex);
            this.layers.push(layer);
            this.zIndex += 1;
            return this;
        }
    });
});