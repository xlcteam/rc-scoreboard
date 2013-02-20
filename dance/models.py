from django.db import models


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
