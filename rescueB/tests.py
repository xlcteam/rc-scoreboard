"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import (Team, Group, Competition, Performance,)
from django.test.client import Client
from django.contrib.auth.models import User


class ModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="testTeam")

        self.ref = User.objects.create_user(username='doe',
                                            email='joe',
                                            password='neno')

        self.round1 = Performance.objects.create(team=self.team, round_number=1, referee=self.ref)
        self.round2 = Performance.objects.create(team=self.team, round_number=2, referee=self.ref)
        self.round3 = Performance.objects.create(team=self.team, round_number=3, referee=self.ref)

        self.group = Group.objects.create(name="testGroup")
        self.group.teams.add(self.team)
        self.group.performances.add(self.round1)
        self.group.performances.add(self.round2)
        self.group.performances.add(self.round3)

        self.competition = Competition.objects.create(name="testCompetition")
        self.competition.groups.add(self.group)

    def test_models(self):
        self.assertEqual(self.team.name, "testTeam")
        self.assertEqual(self.group.name, "testGroup")
        self.assertEqual(self.competition.name, "testCompetition")

        self.assertEqual(self.ref.username, "doe")
        self.assertEqual(self.ref.email, "joe")

        self.assertEqual(self.round1.team, self.team)
        self.assertEqual(self.round2.team, self.team)
        self.assertEqual(self.round3.team, self.team)

        self.assertEqual(self.round1.round_number, 1)
        self.assertEqual(self.round2.round_number, 2)
        self.assertEqual(self.round3.round_number, 3)

        self.assertEqual(self.round1.playing, 'N')
        self.assertEqual(self.round2.playing, 'N')
        self.assertEqual(self.round3.playing, 'N')

        self.assertEqual(self.group.teams.all()[0], self.team)
        self.assertEqual(self.competition.groups.all()[0], self.group)

        self.assertEqual(self.group.performances.all()[0], self.round1)
        self.assertEqual(self.group.performances.all()[1], self.round2)
        self.assertEqual(self.group.performances.all()[2], self.round3)
