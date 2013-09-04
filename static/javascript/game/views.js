define(function(require, exports) {
    'use strict';

    var Backbone = require('backbone')
      , $ = require('jquery')
      , _ = require('underscore')
      , Pusher = require('pusher')
      , collections = require('collections')
      , global = require('global');

    var problemTemplate = require('text!partials/problem.html')
      , problemViewTemplate = require('text!partials/problem-view.html')
      , stageViewTemplate = require('text!partials/stage-view.html')
      , teamViewTemplate = require('text!partials/team-view.html')
      , problemViewer;

    var eventbus = _.extend({}, Backbone.Events);

    var pusher = new Pusher(__pusherKey__);
    var channel = pusher.subscribe('updates');

    channel.bind('submission:start', function(data) {
        if (data.team_id == __teamId__) return;
        eventbus.trigger('submission:start', data.team_id);
    });

    channel.bind('submission:finish', function(data) {
        if (data.team_id == __teamId__) return;
        var team = global.teams.get(data.team_id)
          , oldPos = team.get('position')
          , newPos = data.new_position;

        eventbus.trigger('submission:finish', data.team_id, data.team_points);

        if (data.state == 2 && oldPos && newPos) {
            team.set('position', newPos);
            eventbus.trigger('team:move', team.id, oldPos, newPos);
        }
    });

    channel.bind('team:new', function(data) {
        if (data.id == __teamId__) return;
        global.teams.add(data);
        eventbus.trigger('team:move', data.id, -1, data.position);
    });

    channel.bind('team:move', function(data) {
        eventbus.trigger('team:move', data.team_id, data.old_pos, data.new_pos);
    });

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

        submitSolution: function(e) {
            var self = this
              , $btn = $(e.target)
              , prevHtml = $btn.html()
              , $solution = this.$el.find('.solution textarea')
              , $alert = this.$el.find('.solution .alert');

            if ($solution.val() == '') return;

            // hide the alert box
            $alert.removeClass('alert-success alert-danger').hide();

            // disable the textarea
            $solution.prop('disabled', true).addClass('disabled');

            // disable the submit button
            $btn.prop('disabled', true).addClass('disabled').html('Submitting..');

            // evaluate solution
            $.post('/game/stage/' + this.stage.get('id') + '/submit/', {solution: $solution.val()})
            .done(function(resp) {
                var teamId = self.stage.get('team');

                // trigger UI updates
                self.stage.set({state: resp.state, points_earned: resp.stage_points});

                if (resp.state == 1) {
                    $alert.html('Your solution failed some test cases.').addClass('alert-danger').show();
                } else if (resp.state == 2) {
                    $alert.html('Correct!').addClass('alert-success').show();
                }

                eventbus.trigger('submission:finish', teamId, resp.team_points);
                if (resp.state == 2) eventbus.trigger('stage:next', self.stage);
            })
            .fail(function(err) {
                // TODO
            })
            .always(function() {
                $solution.prop('disabled', false).removeClass('disabled');
                $btn.prop('disabled', false).removeClass('disabled').html(prevHtml);
            })
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
            eventbus.on('team:new', this.updateTeams, this);
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

        updateTeams: function(teamId, oldPos, newPos) {
            if (this.model.get('order') == newPos) {
                this.teamContainerView.addTeam(global.teams.get(teamId));
            } else {
                var existing = this.options.teams.find(function(t) {
                    return t.previousAttributes().position == oldPos;
                });
                if (existing != null) this.teamContainerView.removeTeam(existing);
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
        className: 'team animated fadeInUp clearfix',
        tagName: 'div',
        template: _.template(teamViewTemplate),

        initialize: function() {
            this.listenTo(this.model, 'change:points', this.renderContent);
            eventbus.on({
                'submission:start': this.onSubmissionStart,
                'submission:finish': this.onSubmissionFinish,
            }, this);
        },

        onSubmissionStart: function(teamId) {
            if (teamId != this.model.id) return;
            this.flash();
        },

        onSubmissionFinish: function(teamId, teamPoints) {
            if (teamId != this.model.id) return;
            this.model.set('points', teamPoints);
            this.unflash();
        },

        flash: function() {
            // TODO
        },

        unflash: function() {
            // TODO
        },

        darker: function(hex) {
            var r = parseInt(hex.substring(1, 3), 16)
              , g = parseInt(hex.substring(3, 5), 16)
              , b = parseInt(hex.substring(5, 7), 16)
              , mult = 7/8;
            return _.map([r, g, b], function(t) {
                return parseInt(t * mult);
            });
        },

        render: function() {
            var self = this;
            this.renderContent();
            window.setTimeout(function() {
                self.$el.removeClass('animated fadeInUp');
            }, 1300);
            return this;
        },

        renderContent: function() {
            var bg = this.model.colour()
              , dbg = this.darker(bg)
              , html = this.template({
                    team: this.model.toJSON(),
                    you: __teamId__ == this.model.get('id'),
                    dbg: 'rgb(' + dbg[0] + ',' + dbg[1] + ',' + dbg[2] + ')'
                });
            this.$el.css('background-color', bg).html(html);
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

            eventbus.on('stage:next', this.unlockNextStage, this)
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