define(function(require, exports) {
    'use strict';

    var Backbone = require('backbone')
      , models = require('models');

    exports.TeamCollection = Backbone.Collection.extend({
        model: models.Team
    });

    exports.PositionCollection = Backbone.Collection.extend({
        model: models.Position
    });

    exports.StageCollection = Backbone.Collection.extend({
        model: models.Stage
    });
});