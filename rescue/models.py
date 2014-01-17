from django.db import models
from django import forms
from rescue.forms import *
from rescue.mapmodel import *

class Team(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Performance(models.Model):
    """
        Each team has 3 performances. All of them are stored in group.performances
        and when you want to sort them by a round, just call function group.round_XXX
    """
    team = models.ForeignKey(Team, related_name='performance_rescue')
    round_number = models.IntegerField(default=0)
    referee = models.ForeignKey('auth.User')

    PLAYING_CHOICES = (
        ('N', 'Not performed yet'),
        ('P', 'Being performed at the moment'),
        ('D', 'Already performed (Done)'),
    )

    playing = models.CharField(max_length=1, choices=PLAYING_CHOICES,
        default='N')

    room1 = models.IntegerField(default=0)
    room2 = models.IntegerField(default=0)
    room3 = models.IntegerField(default=0)
    ramp = models.IntegerField(default=0)
    hallway = models.IntegerField(default=0)
    gap = models.IntegerField(default=0)
    obstacle = models.IntegerField(default=0)
    speed_bump = models.IntegerField(default=0)
    intersection = models.IntegerField(default=0)
    victim = models.IntegerField(default=0)
    lift = models.IntegerField(default=0)
    
    points = models.IntegerField(default=0)
    time = models.FloatField(default=0.0)

    finished_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "{0} - {1} round".format(self.team.name, self.round_number)


class Group(models.Model):
    name = models.CharField(max_length=200)
    teams = models.ManyToManyField(Team)
    performances = models.ManyToManyField(Performance)

    # stuff for final table
    result_table_generated = models.BooleanField(default=False)
    perfs_final = models.ManyToManyField(Performance, related_name="final_results")
    # map = models.ForeignKey(SimpleMap)
    RESULTS_CHOICES = (
        ('S', 'Play three rounds - take the sum of the best two as the result (slovak system)'),
        ('D', 'Play two rounds - take the best one as the result (dutch system)'),
    )

    results_type = models.CharField(max_length=1, choices=RESULTS_CHOICES,
        default='S')

    def __unicode__(self):
        return self.name

    def not_played_performances(self):
        return len(self.performances.filter(playing='N'))

    def results_round_1(self):
        return self.performances.filter(round_number=1).order_by('points', '-time').reverse()

    def results_round_2(self):
        return self.performances.filter(round_number=2).order_by('points', '-time').reverse()

    def results_round_3(self):
        return self.performances.filter(round_number=3).order_by('points', '-time').reverse()

    def results_final(self):
        return self.perfs_final.all().order_by('points', '-time').reverse()

class Competition(models.Model):
    name = models.CharField(max_length=200)
    groups = models.ManyToManyField(Group)

    def __unicode__(self):
        return self.name


class NewEventForm(forms.Form):
    name = forms.CharField(max_length=30)

#   class NewGroupForm(forms.Form):
#       name = forms.CharField(max_length=30)

#       RESULTS_CHOICES = (
#           ('S', 'Play three rounds - take the sum of the best two as the result (slovak system)'),
#           ('D', 'Play two rounds - take the best one as the result (dutch system)'),
#       )

#       results_type = forms.ChoiceField(choices=RESULTS_CHOICES)

class NewGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'results_type']


class NewTeamForm(forms.Form):
    names = forms.CharField(widget=forms.Textarea(attrs={'size':'20'}))

class MatchSaveForm(forms.Form):
    room1 = forms.IntegerField(label='Room 1 (try)')
    room2 = forms.IntegerField(label='Room 2 (try)')
    room3 = forms.IntegerField(label='Room 3 (try)')
    ramp = forms.IntegerField(label='Ramp (try)')
    hallway = forms.IntegerField(label='Hallway (try)')
    victim = forms.IntegerField(label='Victim (try)')
    gap = forms.IntegerField(label='Gap')
    obstacle = forms.IntegerField(label='Obstacle')
    speed_bump = forms.IntegerField(label='Speed Bump')
    intersection = forms.IntegerField(label='Intersection')
    lift = forms.IntegerField(label="Lift (secondary)")
    points = forms.IntegerField(label='Points')
    time = forms.CharField(label='Time')
    
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                max_length=100)

