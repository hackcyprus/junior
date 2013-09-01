define(function(require, exports) {
    'use strict';

    var Backbone = require('backbone')
      , global = require('global');

    exports.Team = Backbone.Model.extend({});
    exports.Position = Backbone.Model.extend({});
    exports.Stage = Backbone.Model.extend({
        states: {
            0: 'Not Tried',
            1: 'Tried But Failed',
            2: 'Solved Correctly',
            3: 'Skipped'
        },

        getHumanState: function() {
            return this.states[this.get('state')];
        },

        getProblemOrder: function() {
            var problem = global.positions.get(this.get('problem'));
            return problem.get('order');
        }
    });
});