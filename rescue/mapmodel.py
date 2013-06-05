from django.db import models
from django import forms

class Tile(models.Model):
    points = 0

class GapTile(Tile):
    points = 10

class ObstacleTile(Tile):
    points = 10

class SpeedbumpTile(Tile):
    points = 10
