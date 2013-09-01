from django.contrib import admin
from .models import Problem, Stage, Attempt, Game


class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'started_on')
    actions = ['start_games']

    def start_games(self, request, queryset):
        for game in queryset.all():
            game.start()
        self.message_user(request, 'The selected games are now started.')
    start_games.short_description = 'Start selected games'


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'order', 'base_points', 'multiplier')


class StageAdmin(admin.ModelAdmin):
    list_display = ('problem', 'team', 'unlocked_on', 'points_earned', 'state')


class AttemptAdmin(admin.ModelAdmin):
    list_display = ('stage', 'correct', 'created')


admin.site.register(Game, GameAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Attempt, AttemptAdmin)