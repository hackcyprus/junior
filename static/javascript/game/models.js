define(function(require, exports) {
    'use strict';

    var Backbone = require('backbone')
      , global = require('global');

    var teamColours = [
        '#FFBBBB', '#FFE1BA', '#FDFFBA', '#D6FFBA',
        '#BAFFCE', '#BAFFFD', '#BAE6FF', '#BAC8FF',
        '#D3BAFF', '#EBBAFF', '#E4E0FF', '#BAFCE1',
        '#FCC6BB', '#E3F3CE', '#EEEEEE', '#D8FFF4'
    ];

    exports.Problem = Backbone.Model.extend({});

    exports.Team = Backbone.Model.extend({
        colour: function() {
            return teamColours[this.id % teamColours.length];
        }
    });

    exports.Stage = Backbone.Model.extend({
        glyphs: {
            1: 'remove',
            2: 'ok',
            3: 'forward'
        },

        glyph: function() {
            return this.glyphs[this.get('state')];
        }
    });
});