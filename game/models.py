from django.db import models
from django.utils.timezone import now
from teams.models import Team


class Problem(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField()
    html_template = models.CharField(max_length=100)
    multiplier = models.FloatField(default=1.0)
    base_points = models.IntegerField(default=300)
    created = models.DateTimeField(default=now)

    def __unicode__(self):
        return self.name


class Stage(models.Model):
    """A stage is a place in the game. Each problem represents a stage for each
    team. A stage N is normally locked, until the team solves N-1 correctly.
    """
    unlocked_on = models.DateTimeField(null=True, blank=True)
    points_earned = models.FloatField(default=0)
    problem = models.ForeignKey(Problem)
    team = models.ForeignKey(Team)
    created = models.DateTimeField(default=now)

    @property
    def locked(self):
        return self.unlocked_on is None

    def unlock(self, save=True):
        self.unlocked_on = now()
        if save: self.save()


class Attempt(models.Model):
    """An attempt to solve/pass a stage. Each attempt records the outcome and
    the error percentage for analytics.
    """
    correct = models.BooleanField()
    stage = models.ForeignKey(Stage)
    created = models.DateTimeField(default=now)
