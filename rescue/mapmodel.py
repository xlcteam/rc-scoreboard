from django.db import models
from django import forms

class Tile(models.Model):
    points = 0
    completed = models.BooleanField(initial=False)
    image = models.CharField(max_length=60)
    rotation = models.IntegerField()

class GapTile(Tile):
    points = 10

class ObstacleTile(Tile):
    points = 10

class SpeedbumpTile(Tile):
    points = 10


class Map(models.Model):
    name = models.CharField(max_length=60)
    tiles = models.ManyToManyField(Tile)

    def score(self):
       
        scoresum = 0

        def cout_up_score(tile):
            scoresum += tile.points if tile.completed

        map(cout_up_score, self.tiles)

        return scoresum


    

