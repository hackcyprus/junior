import uuid
from django.db import models
from django.utils.timezone import now


class Team(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(default=now)
    token = models.CharField(max_length=32, default=lambda: uuid.uuid4().hex)

    @property
    def latest_stage(self):
        return self.stages.filter(unlocked_on__isnull=False).order_by('problem__order')[0]

    @property
    def total_points(self):
        return sum(stage.points_earned for stage in self.stages.all())

    def __unicode__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name,
            'token': self.token
        }


class Participant(models.Model):
    name = models.CharField(max_length=150)
    team = models.ForeignKey(Team)
    created = models.DateTimeField(default=now)

    def __unicode__(self):
        return self.name
