from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class SimpleMap(models.Model):
    data = models.TextField()
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name


class SimpleRun(models.Model):
    map = models.ForeignKey(SimpleMap)
    round_number = models.IntegerField(default=0)
    referee = models.ForeignKey('auth.User', related_name='simplerun_rescueb')
    team = models.ForeignKey(Team, related_name='simplerun_rescueb')

    points = models.IntegerField(default=0)
    time = models.FloatField(default=0.0)

    finished_at = models.DateTimeField(auto_now=True)
