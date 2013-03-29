from django.db import models
from django import forms

class NewEventForm(forms.Form):
    name = forms.CharField(max_length=30)

class NewTeamForm(forms.Form):
    names = forms.CharField(widget=forms.Textarea(attrs={'size':'20'}))

class Team(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Performance(models.Model):
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
    gaps = models.IntegerField(default=0)
    obstacles = models.IntegerField(default=0)
    speed_bumps = models.IntegerField(default=0)
    intersections = models.IntegerField(default=0)
    victim = models.IntegerField(default=0)

    points = models.IntegerField(default=0)
    time = models.FloatField(default=0.0)


class Group(models.Model):
    name = models.CharField(max_length=200)
    teams = models.ManyToManyField(Team)
    performances = models.ManyToManyField(Performance)

    def __unicode__(self):
        return self.name

    def round_1(self):
        return self.performances.filter(round_number=1).order_by(points).order_by(time).reverse()

    def round_2(self):
        return self.performances.filter(round_number=2).order_by(points).order_by(time).reverse()

    def round_3(self):
        return self.performances.filter(round_number=3).order_by(points).order_by(time).reverse()


class Competition(models.Model):
    name = models.CharField(max_length=200)
    groups = models.ManyToManyField(Group)

    def __unicode__(self):
        return self.name


