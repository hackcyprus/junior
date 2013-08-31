from django.contrib import admin
from django.shortcuts import redirect
from .models import Team, Participant


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'token', 'created')
    actions = ['make_active_in_session']

    def make_active_in_session(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, 'You can only make one team active!')
        else:
            team = queryset[0]
            response = redirect(request.path)
            response.set_signed_cookie('jhteam', team.token)
            self.message_user(request, "Team '{}' is now active in this session.".format(team.name))
            return response
    make_active_in_session.short_description = 'Make team active in session'


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'created')


admin.site.register(Team, TeamAdmin)
admin.site.register(Participant, ParticipantAdmin)