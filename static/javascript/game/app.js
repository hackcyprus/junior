define(function(require, exports) {
    'use strict';

    var backbone = require('backbone')
      , $ = require('jquery')
      , views = require('views')
      , collections = require('collections')
      , global = require('global');

    var teams = new collections.TeamCollection()
      , positions = new collections.PositionCollection()
      , stages = new collections.StageCollection()
      , map = new views.MapView()

    global.positions = positions;
    global.stages = stages;
    global.teams = teams;

    var bootstrap = function() {
        teams.reset(BOOTSTRAP.teams);
        stages.reset(BOOTSTRAP.stages);
        // TODO: correlate this to pre-defined map positions
        positions.reset(BOOTSTRAP.problems);
    };

    var configureCSRF = function() {
        $.ajaxSetup({
            headers: {
                'X-CSRFToken': $('#csrf-token').val()
            }
        });
    };

    exports.initialize = function() {
        bootstrap();
        configureCSRF();

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