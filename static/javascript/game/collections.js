define(function(require, exports) {
    'use strict';

    var Backbone = require('backbone')
      , models = require('models');

    exports.TeamCollection = Backbone.Collection.extend({
        model: models.Team
    });

    exports.ProblemCollection = Backbone.Collection.extend({
        model: models.Problem
    });

    exports.StageCollection = Backbone.Collection.extend({
        model: models.Stage,

        after: function(stage){
            var order = stage.get('problem_order');
            return this.find(function(s) {
                return s.get('problem_order') == order + 1;
            });
        }
    });
});