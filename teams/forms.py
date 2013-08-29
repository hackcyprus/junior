from django import forms
from django.core.exceptions import ValidationError
from .models import Team


class TeamForm(forms.Form):
    name = forms.CharField(max_length=100)
    participants = forms.CharField(widget=forms.Textarea)

    def clean_name(self):
        name = self.cleaned_data['name']
        if Team.objects.filter(name=name).exists():
            raise ValidationError("A team with name '{}' already exists.".format(name))
        return name

    def clean_participants(self):
        participants = self.cleaned_data['participants']
        return [p for p in map(unicode.strip, participants.split()) if p]