define(function(require, exports) {
    'use strict';

    var backbone = require('backbone')
      , views = require('views')
      , collections = require('collections')
      , global = require('global');

    var teams = new collections.TeamCollection()
      , positions = new collections.PositionCollection()
      , stages = new collections.StageCollection()
      , map = new views.MapView()

    global.positions = positions;

    var bootstrap = function() {
        teams.reset(BOOTSTRAP.teams);
        stages.reset(BOOTSTRAP.stages);
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

        // draw stages
        map.addLayer(new views.StageLayer({
            collection: stages
        }));

        map.render();
    };
});