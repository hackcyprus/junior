define(function(require, exports) {
    'use strict';

    var Backbone = require('backbone')
      , $ = require('jquery')
      , _ = require('underscore')
      , global = require('global');

    var problemTemplate = require('text!partials/problem.html')
      , problemViewer;

    var ProblemViewer = Backbone.View.extend({
        el: '#problem-viewer',

        template: _.template(problemTemplate),

        open: function(stage) {
            var self = this
              , problem = global.positions.get(stage.get('problem'))
              , title = '#' + problem.get('order') + ' ' + problem.get('name')
              , downloadUrl = '/game/stage/' + stage.get('id') + '/download/';
            self.$el.find('.modal-title').html(title);
            self.$el.find('#download-test-file').attr('href', downloadUrl);
            self.$el.modal('show');

            $.get('/game/stage/' + stage.get('id'), function(data) {
                self.$el.find('.modal-body').html(self.template(data));
            }, 'json');
        }
    });

    problemViewer = new ProblemViewer();

    var PositionView = Backbone.View.extend({
        className: 'thing position',
        render: function() {
            this.$el.html(this.model.get('name'));
            return this;
        }
    });

    var TeamView = Backbone.View.extend({
        className: 'thing team',
        render: function() {
            this.$el.html(this.model.get('name') + ' <b>(' + this.model.get('position') + ')</b>');
            return this;
        }
    });

    var StageView = Backbone.View.extend({
        className: 'thing stage',

        events: {
            'click': 'openProblem'
        },

        render: function() {
            var klass = this.model.get('locked') ? 'locked' : 'unlocked';
            this.$el.html('#' + this.model.get('problem')).addClass(klass);
            return this;
        },

        openProblem: function() {
            if (this.model.get('locked')) return;
            problemViewer.open(this.model);
        }
    });

    var Layer = Backbone.View.extend({
        childView: null,
        className: 'layer',

        initialize: function() {
            this.children = [];
        },

        render: function() {
            this.collection.each(this.addChild, this);
            return this;
        },

        addChild: function(child) {
            if (this.childView == null) throw new Error('childView is undefined!');
            var view = new this.childView({model: child});
            this.children.push(view);
            this.$el.append(view.render().$el);
        }
    });

    exports.PositionLayer = Layer.extend({
        childView: PositionView
    });

    exports.TeamLayer = Layer.extend({
        childView: TeamView
    });

    exports.StageLayer = Layer.extend({
        childView: StageView
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