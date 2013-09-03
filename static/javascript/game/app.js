define(function(require, exports) {
    'use strict';

    var backbone = require('backbone')
      , $ = require('jquery')
      , views = require('views')
      , collections = require('collections')
      , global = require('global');

    var teams = new collections.TeamCollection()
      , problems = new collections.ProblemCollection()
      , stages = new collections.StageCollection();

    global.problems = problems;
    global.stages = stages;
    global.teams = teams;

    var bootstrap = function() {
        teams.reset(BOOTSTRAP.teams);
        stages.reset(BOOTSTRAP.stages);
        problems.reset(BOOTSTRAP.problems);
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
        var game = new views.GameView({
            problems: global.problems,
            teams: global.teams,
            stages: global.stages
        });
        game.render();
    };
});