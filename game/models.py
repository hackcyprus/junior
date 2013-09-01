from django.db import models
from django.utils.timezone import now
from teams.models import Team


class Problem(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField()
    description = models.TextField()
    io_description = models.TextField('I/O Description')
    sample_in = models.TextField()
    sample_out = models.TextField()
    multiplier = models.FloatField(default=1.0)
    base_points = models.IntegerField(default=300)
    test_file = models.FileField(upload_to='testfiles', null=True, blank=True)
    created = models.DateTimeField(default=now)

    def __unicode__(self):
        return self.name


class Stage(models.Model):
    """A stage is a place in the game. Each problem represents a stage for each
    team. A stage N is normally locked, until the team solves N-1 correctly.
    """
    unlocked_on = models.DateTimeField(null=True, blank=True)
    points_earned = models.FloatField(default=0)
    problem = models.ForeignKey(Problem, related_name='problems')
    team = models.ForeignKey(Team, related_name='stages')
    created = models.DateTimeField(default=now)

    @property
    def locked(self):
        return self.unlocked_on is None

    def unlock(self, save=True):
        self.unlocked_on = now()
        if save: self.save()

    def to_dict(self):
        return {
            'id': self.id,
            'locked': self.locked,
            'unlocked_on': self.unlocked_on,
            'points_earned': self.points_earned,
            'problem': self.problem_id,
            'team': self.team_id
        }


class Attempt(models.Model):
    """An attempt to solve/pass a stage. Each attempt records the outcome and
    the error percentage for analytics.
    """
    correct = models.BooleanField()
    stage = models.ForeignKey(Stage)
    created = models.DateTimeField(default=now)
