from django.contrib import admin
from .models import Team, Participant


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'created')


admin.site.register(Team, TeamAdmin)
admin.site.register(Participant, ParticipantAdmin)