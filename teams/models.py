import uuid
from django.db import models
from django.utils.timezone import now


class Team(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(default=now)
    token = models.CharField(max_length=32, default=lambda: uuid.uuid4().hex)

    def __unicode__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=150)
    team = models.ForeignKey(Team)
    created = models.DateTimeField(default=now)

    def __unicode__(self):
        return self.name