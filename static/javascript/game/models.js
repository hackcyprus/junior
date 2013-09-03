define(function(require, exports) {
    'use strict';

    var Backbone = require('backbone');

    exports.Team = Backbone.Model.extend({});
    exports.Problem = Backbone.Model.extend({});
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