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

    var eventbus = _.extend({}, Backbone.Events);

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
                eventbus.trigger('stage:solved', self.stage);
            })
            .fail(function(err) {
                // TODO: handle err
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
            this.teamContainerView = null;
            this.listenTo(this.options.stage, 'change:locked', this.renderLockState);

            eventbus.on('team:move', this.updateTeams, this);
        },

        render: function() {
            _.bindAll(this, 'renderLockState');

            var html = this.template(this.model.toJSON())
              , stageView = new StageView({model: this.options.stage})
              , $el = this.$el;

            this.teamContainerView = new TeamContainerView({teams: this.options.teams});

            $el.html(html);
            $el.find('.stage').html(stageView.render().$el);
            $el.find('.teams').html(this.teamContainerView.render().$el);

            this.renderLockState(this.options.stage);

            return this;
        },

        renderLockState: function(stage) {
            stage.get('locked') ? this.$el.addClass('locked') : this.$el.removeClass('locked');
        },

        openProblem: function() {
            if (this.model.get('locked')) return;
            problemViewer.open(this.model, this.options.stage);
        },

        updateTeams: function(team, oldPos, newPos) {
            if (this.model.get('order') == newPos) {
                this.teamContainerView.addTeam(team);
            } else {
                var existing = this.options.teams.find(function(t) {
                    return t.previousAttributes().position == oldPos;
                });
                if (existing != null) this.teamContainerView.removeTeam(team);
            }
        }
    });

    var TeamContainerView = Backbone.View.extend({
        initialize: function() {
            this.children = [];
            this.teams = this.options.teams;
        },

        render: function() {
            _.bindAll(this, 'addTeam', 'removeTeam');

            var self = this;

            if (this.teams.size() == 0) {
                this.renderEmpty();
            } else {
                this.teams.each(this.addTeam);
            }
            return this;
        },

        renderEmpty: function() {
            this.$el.html('<span>Nobody is here.</span>');
            return this;
        },

        clean: function() {
            this.$el.empty();
            return this;
        },

        removeTeam: function(team) {
            var self = this
              , view = _.find(this.children, function(t) {
                    return t.model.id == team.id;
                });

            view.$el.addClass('animated fadeOutDown');
            window.setTimeout(function() {
                view.remove();
                if (self.teams.size() == 0) self.renderEmpty();
            }, 1300);

            this.teams.remove(team);
        },

        addTeam: function(team) {
            if (this.teams.size() == 0) this.clean();
            var view = new TeamView({model: team});
            this.children.push(view);
            view.render().$el.addClass('animated fadeInUp');
            this.$el.append(view.render().$el);
            this.teams.add(team);
        }
    });

    var TeamView = Backbone.View.extend({
        className: 'team animated fadeInUp',
        tagName: 'span',

        render: function() {
            var self = this;
            this.$el.html(this.model.get('name'));
            window.setTimeout(function() {
                self.$el.removeClass('animated fadeInUp');
            }, 1300);
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

            eventbus.on('stage:solved', this.unlockNextStage, this)
        },

        unlockNextStage: function(stage) {
            var nextStage = this.stages.after(stage)
              , team = this.teams.get(stage.get('team'))
              , oldPos = team.get('position');
            if (nextStage != null && nextStage.get('locked')) {
                nextStage.set('locked', false);
                team.set('position', nextStage.get('problem_order'));
                eventbus.trigger('team:move', team, oldPos, team.get('position'));
            }
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