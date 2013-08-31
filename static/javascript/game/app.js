define(function(require, exports) {
    'use strict';

    var backbone = require('backbone')
      , views = require('views')
      , collections = require('collections');

    var teams = new collections.TeamCollection()
      , positions = new collections.PositionCollection()
      , map = new views.MapView()

    var bootstrap = function() {
        teams.reset(BOOTSTRAP.teams);
        // TODO: correlate this to pre-defined map positions
        positions.reset(BOOTSTRAP.problems);
    };

    exports.initialize = function() {
        bootstrap();

        // draw all positions
        map.addLayer(new views.PositionLayer({
            collection: positions
        }));

        // draw teams
        map.addLayer(new views.TeamLayer({
            collection: teams
        }));

        map.render();
    };
});