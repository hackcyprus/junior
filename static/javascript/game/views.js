define(function(require, exports) {
    'use strict';

    var Backbone = require('backbone')
      , $ = require('jquery')
      , _ = require('underscore')
      , collections = require('collections')
      , global = require('global');

    var problemTemplate = require('text!partials/problem.html')
      , problemViewTemplate = require('text!partials/problem-view.html')
      , stageViewTemplate = require('text!partials/stage-view.html')
      , problemViewer;

    var ProblemViewer = Backbone.View.extend({
        el: '#problem-viewer',

        template: _.template(problemTemplate),

        events: {
            'click #submit-solution ': 'submitSolution'
        },

        initialize: function() {
            this.stage = null;
            this.deferred = null;
        },

        open: function(problem, stage) {
            this.stage = stage;
            this.deferred = $.Deferred();

            var title = '#' + problem.get('order') + ' ' + problem.get('name')
              , downloadUrl = '/game/stage/' + stage.get('id') + '/download/';

            this.$el.find('.modal-title').html(title);
            this.$el.find('#download-test-file').attr('href', downloadUrl);
            this.$el.modal('show');

            var self = this;
            $.get('/game/stage/' + stage.get('id') + '/', function(data) {
                self.$el.find('.modal-body').html(self.template(data));
            }, 'json');

            return this.deferred.promise();
        },

        submitSolution: function() {
            var self = this;
            $.post('/game/stage/' + this.stage.get('id') + '/submit/')
            .done(function(resp) {
                self.stage.set({state: resp.state, points_earned: resp.points});
                self.deferred.resolve(resp);
            })
            .fail(function(err) {
                // TODO: handle err
                self.deferred.reject(err);
            });
        }
    });

    problemViewer = new ProblemViewer();

    var ProblemView = Backbone.View.extend({
        className: 'problem',

        events: {
            'click .footer button': 'openProblem'
        },

        template: _.template(problemViewTemplate),

        initialize: function() {
            this.stages = this.options.stages;
            this.listenTo(this.options.teams, 'change', function(team) {
                console.log(team);
            });
            this.listenTo(this.options.stage, 'change:locked', this.renderLockState);
        },

        render: function() {
            _.bindAll(this, 'renderLockState', 'unlockNextStage');

            var html = this.template(this.model.toJSON())
              , stageView = new StageView({model: this.options.stage})
              , teamContainerView = new TeamContainerView({teams: this.options.teams})
              , $el = this.$el;

            $el.html(html);
            $el.find('.stage').html(stageView.render().$el);
            $el.find('.teams').append(teamContainerView.render().$el);

            this.renderLockState(this.options.stage);

            return this;
        },

        unlockNextStage: function(resp) {
            var stage = this.options.stage
              , nextStage = global.stages.after(stage)
              , team = global.teams.get(stage.get('team'));
            if (nextStage != null && nextStage.get('locked')) {
                nextStage.set('locked', false);
                team.set('position', nextStage.get('problem_order'));
            }
        },

        renderLockState: function(stage) {
            stage.get('locked') ? this.$el.addClass('locked') : this.$el.removeClass('locked');
        },

        openProblem: function() {
            if (this.model.get('locked')) return;
            var promise = problemViewer.open(this.model, this.options.stage);
            promise.done(this.unlockNextStage).fail(function() {
                // TODO
            });
        }
    });

    var TeamContainerView = Backbone.View.extend({
        initialize: function() {
            this.children = [];
            this.teams = this.options.teams;
        },

        render: function() {
            var self = this;
            if (this.teams.size() == 0) {
                this.$el.html('<span>Nobody is here.</span>');
            } else {
                this.teams.each(function(team) {
                    var view = new TeamView({model: team});
                    self.children.push(view);
                    self.$el.append(view.render().$el);
                });
            }
            return this;
        }
    });

    var TeamView = Backbone.View.extend({
        className: 'team',
        tagName: 'span',

        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
        },

        render: function() {
            this.$el.html(this.model.get('name'));
            return this;
        }
    });

    var StageView = Backbone.View.extend({
        template: _.template(stageViewTemplate),

        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
        },

        render: function() {
            var html = this.template({
                glyph: this.model.glyph(),
                klass: this.model.get('state') == 1 ? 'wrong' : 'ok',
                stage: this.model.toJSON()
            });
            this.$el.html(html);
            return this;
        }
    });

    exports.GameView = Backbone.View.extend({
        el: '#game',
        className: 'game',

        initialize: function() {
            this.children = [];
            this.problems = this.options.problems;
            this.stages = this.options.stages;
            this.teams = this.options.teams;
        },

        render: function() {
            var self = this;
            this.problems.each(function(problem) {
                var order = problem.get('order')
                  , teamsAtProblem = self.teams.filter(function(team) {
                        return team.get('position') == order;
                    })
                  , stage = self.stages.find(function(stage) {
                        return stage.get('problem_order') == order;
                    })
                  , pv = new ProblemView({
                        model: problem,
                        stage: stage,
                        teams: new collections.TeamCollection(teamsAtProblem)
                    });

                self.children.push(pv);
                self.$el.append(pv.render().$el);
            });
            return this;
        }
    });
});