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
    team = models.ForeignKey(Team, related_name='homelanders')
    PLAYING_CHOICES = (
        ('N', 'Not performed yet'),
        ('P', 'Being performed at the moment'),
        ('D', 'Already performed (Done)'),
    )
    playing = models.CharField(max_length=1, choices=PLAYING_CHOICES,
            default='N')
    referee = models.ForeignKey('auth.User')

    class Meta:
        verbose_name_plural = 'performances'

    def __unicode__(self):
        return "%s" % (self.team.name,)

class TeamResult(models.Model):
    team = models.ForeignKey(Team)

    performances_played = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    # NOTE: time in seconds
    time = models.FloatField(default=0.0)

    def __unicode__(self):
        return "{0} - {1} - {2} -> {3}".format(self.wins, self.draws,
                self.loses, self.team)

class Group(models.Model):
    name = models.CharField(max_length=200)
    teams = models.ManyToManyField(Team)
    performances = models.ManyToManyField(Performance)
    results = models.ManyToManyField(TeamResult)

    actual_round = models.IntegerField(default=0) # NOTE: 0 == performances not generated

    def __unicode__(self):
        return self.name


class Competition(models.Model):
    name = models.CharField(max_length=200)
    groups = models.ManyToManyField(Group)

    def __unicode__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    competitions = models.ManyToManyField(Competition)

    def __unicode__(self):
        return self.name

