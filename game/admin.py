from django.contrib import admin
from .models import Problem, Stage, Attempt


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'base_points', 'multiplier')


class StageAdmin(admin.ModelAdmin):
    list_display = ('unlocked_on', 'points_earned', 'problem', 'team')


class AttemptAdmin(admin.ModelAdmin):
    list_display = ('stage', 'correct', 'created')


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Attempt, AttemptAdmin)