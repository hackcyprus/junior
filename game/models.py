from django.db import models
from django.utils.timezone import now
from teams.models import Team


class Game(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    started_on = models.DateTimeField(null=True, blank=True)

    @property
    def started(self):
        return self.started_on is not None

    def start(self, save=True):
        self.started_on = now()
        if save: self.save()

    def __unicode__(self):
        return self.name


class Problem(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField()
    pdf_gr = models.FileField(upload_to='pdfs', null=True, blank=True)
    pdf_en = models.FileField(upload_to='pdfs', null=True, blank=True)
    io_description = models.TextField('I/O Description')
    sample_in = models.TextField()
    sample_out = models.TextField()
    multiplier = models.FloatField(default=1.0)
    base_points = models.IntegerField(default=300)
    in_file = models.FileField(upload_to='testfiles', null=True, blank=True)
    out_file = models.FileField(upload_to='testfiles', null=True, blank=True)
    game = models.ForeignKey(Game, null=True, blank=True)
    created = models.DateTimeField(default=now)

    def __unicode__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'order': self.order
        }


class Stage(models.Model):
    """A stage is a place in the game. Each problem represents a stage for each
    team. A stage N is normally locked, until the team solves N-1 correctly.
    """
    # Stage states
    NOT_TRIED = 0
    TRIED_BUT_FAILED = 1
    SOLVED_CORRECTLY = 2
    SKIPPED = 3

    unlocked_on = models.DateTimeField(null=True, blank=True)
    state = models.IntegerField(default=NOT_TRIED, choices=[
        (NOT_TRIED, 'Not Tried'),
        (TRIED_BUT_FAILED, 'Tried But Failed'),
        (SOLVED_CORRECTLY, 'Solved Correctly'),
        (SKIPPED, 'Skipped')
    ])
    points_earned = models.FloatField(default=0)
    problem = models.ForeignKey(Problem, related_name='problems')
    team = models.ForeignKey(Team, related_name='stages')
    created = models.DateTimeField(default=now)

    @property
    def locked(self):
        return self.unlocked_on is None

    @property
    def next(self):
        order = self.problem.order
        try:
            return self.team.stages.get(problem__order=order + 1)
        except Stage.DoesNotExist:
            return None

    def unlock(self, save=True):
        self.unlocked_on = now()
        if save: self.save()

    def to_dict(self):
        problem = self.problem
        return {
            'id': self.id,
            'locked': self.locked,
            'state': self.state,
            'unlocked_on': self.unlocked_on,
            'points_earned': self.points_earned,
            'problem': problem.id,
            'problem_order': problem.order,
            'team': self.team_id
        }


class Attempt(models.Model):
    """An attempt to solve/pass a stage. Each attempt records the outcome and
    the error percentage for analytics.
    """
    solution = models.TextField(null=True, blank=True)
    correct = models.BooleanField()
    stage = models.ForeignKey(Stage)
    created = models.DateTimeField(default=now)
