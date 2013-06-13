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
    RESULTS_CHOICES = (
        ('S', 'Play three rounds - take the sum of the best two as the result (slovak system)'),
        ('D', 'Play two rounds - take the best one as the result (dutch system)'),
    )

    results_type = models.CharField(max_length=1, choices=RESULTS_CHOICES,
        default='S')

    def __unicode__(self):
        return self.name

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
