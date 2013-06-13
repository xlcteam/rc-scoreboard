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

    def score(self):
       
        scoresum = 0

        def cout_up_score(tile):
            if tile.completed:
                scoresum += tile.points 

        map(cout_up_score, self.tiles)

        return scoresum
    
