from django.db import models
from django import forms

class Tile(models.Model):
    points = 0
    completed = models.BooleanField(default=False)
    image = models.CharField(max_length=60)
    rotation = models.IntegerField(default=0)

class GapTile(Tile):
    points = 10

class ObstacleTile(Tile):
    points = 10

class SpeedbumpTile(Tile):
    points = 10


class Map(models.Model):
    name = models.CharField(max_length=60)
    tiles = models.ManyToManyField(Tile)

    room1_tries = models.IntegerField(default=0)
    room2_tries = models.IntegerField(default=0)
    room3_tries = models.IntegerField(default=0)

    ramp_tries = models.IntegerField(default=0)
    hallway_tries = models.IntegerField(default=0)
    victim_tries = models.IntegerField(default=0)

    
class Run(models.Model):

    map = models.ForeignKey(Map)

    def score(self):
       
        scores = {
            'room1' : {0: 0, 1 : 60, 2 : 40, 3 : 20},
            'room2' : {0: 0, 1 : 60, 2 : 40, 3 : 20},
            'room3' : {0: 0, 1 : 60, 2 : 40, 3 : 20},
            'ramp'  : {0: 0, 1 : 30, 2 : 20, 3 : 10},
            'hallway':{0: 0, 1 : 30, 2 : 20, 3 : 10},
            'victim': {0: 0, 1 : 60, 2 : 40, 3 : 20},      
        }

        scoresum = 0

        def count_up_score(tile):
            if tile.completed:
                scoresum += tile.points 


        map(count_up_score, self.tiles)

        def count_up_tries(type, tries):
            if tries < 0 and tries > 3:
                return 0
            else:
                return scores[type][tries]
        
        
        scoresum += count_up_tries('room1', self.room1_tries)
        scoresum += count_up_tries('room2', self.room2_tries)
        scoresum += count_up_tries('room3', self.room3_tries)

        scoresum += count_up_tries('ramp', self.ramp_tries)
        scoresum += count_up_tries('hallway', self.hallway_tries)
        scoresum += count_up_tries('victim', self.victim_tries)

        return scoresum


class Team(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class SimpleMap(models.Model):
    data = models.TextField()

class SimpleRun(models.Model):
    map = models.ForeignKey(SimpleMap)
    round_number = models.IntegerField(default=0)
    referee = models.ForeignKey('auth.User')
    team = models.ForeignKey(Team, related_name='simplerun_rescue')

    points = models.IntegerField(default=0)
    time = models.FloatField(default=0.0)

    finished_at = models.DateTimeField(auto_now=True)
 

