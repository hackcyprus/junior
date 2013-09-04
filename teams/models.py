import uuid
from collections import defaultdict

from django.db import models
from django.utils.timezone import now


class Team(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(default=now)
    token = models.CharField(max_length=32, default=lambda: uuid.uuid4().hex)

    @property
    def latest_stage(self):
        return self.stages.filter(unlocked_on__isnull=False).order_by('-problem__order')[0]

    @property
    def total_points(self):
        return sum(stage.points_earned for stage in self.stages.all())

    def __unicode__(self):
        return self.name

    def attempt_stats(self):
        counts = defaultdict(int)
        for stage in self.stages.all():
            counts[stage.state] += 1
        return tuple(counts[i] for i in range(4))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.latest_stage.problem.order,
            'points': self.total_points
        }


class Participant(models.Model):
    name = models.CharField(max_length=150)
    team = models.ForeignKey(Team)
    created = models.DateTimeField(default=now)

    def __unicode__(self):
        return self.name
