"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from .models import (Event, Competition, Group, Team)
from django.test.client import Client

#class SimpleTest(TestCase):
#    def test_basic_addition(self):
#        """
#        Tests that 1 + 1 always equals 2.
#        """
#        self.assertEqual(1 + 1, 2)


class ModelTest(TestCase):
    def setup(self):
        self.client = Client()

    def test_models(self):
        #self.teamA = Team.objects.create(name="test_dance_teamA")
        #self.teamB = Team.objects.create(name="test_dance_teamB")
        #self.group = Group.objects.create(name="test_dance_group", teams=[self.teamA, self.teamB])
        #self.competition = Competition.objects.create(name="test_dance_competition", groups=[self.group])
        #self.event = Event.objects.create(name="test_dance_event", competitions=[self.competition])
        pass
         


