"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import (Team, Group, Competition, Match,
        TeamResult, MatchSaveForm)
from django.test.client import Client
from django.contrib.auth.models import User

#   class SimpleTest(TestCase):
#       def test_basic_addition(self):
#           """
#           Tests that 1 + 1 always equals 2.
#           """
#           self.assertEqual(1 + 1, 2)


class ModelTest(TestCase):

    def setUp(self):
        self.teamA = Team.objects.create(name="testTeamA")
        self.teamB = Team.objects.create(name="testTeamB")

        self.resultA = TeamResult.objects.create(team=self.teamA)
        self.resultB = TeamResult.objects.create(team=self.teamB)

        ref = User.objects.create_user(username='joe',
                                       email='doe',
                                       password='none')

        self.match = Match.objects.create(teamA=self.teamA,
                                          teamB=self.teamB,
                                          referee=ref)

        self.group = Group.objects.create(name="testGroup",
                                          teams=[self.teamA, self.teamB],
                                          matches=[self.match],
                                          results=[self.resultA, self.resultB])

        self.competition = Competition.objects.create(name="testCompetition",
                                                      groups=[self.group])

        self.event = Event.objects.create(name="testEvent",
                                          competitions=[self.competition])

    def test_models(self):

        self.assertEqual(self.teamA.name, "testTeamA")
        self.assertEqual(self.teamB.name, "testTeamB")

        self.assertEqual(self.)


