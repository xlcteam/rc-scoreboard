from django.db import models
from django import forms

class NewEventForm(forms.Form):
    name = forms.CharField(max_length=30)

class Team(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=200)
    teams = models.ManyToManyField(Team)

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

    def __unicode__(self):
        return "%s" % (self.team.name,)
