from django.db import models
from django import forms
from django.forms import ModelForm

class NewEventForm(forms.Form):
    name = forms.CharField(max_length=30)

class NewTeamForm(forms.Form):
    names = forms.CharField(widget=forms.Textarea(attrs={'size':'20'}))


class MatchSaveForm(forms.Form):
    scoreA = forms.IntegerField(label='Score of team A')
    scoreB = forms.IntegerField(label='Score of team B')
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                max_length=100)


class Team(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Match(models.Model):
    teamA = models.ForeignKey(Team, related_name='homelanders')
    teamB = models.ForeignKey(Team, related_name='foreigners')
    scoreA = models.IntegerField(default=0)
    scoreB = models.IntegerField(default=0)
    PLAYING_CHOICES = (
        ('N', 'Not played yet (To be played)'),
        ('P', 'Playing at the moment (Match in progress)'),
        ('D', 'Already played (Done)'),
    )
    playing = models.CharField(max_length=1, choices=PLAYING_CHOICES,
            default='N')
    referee = models.ForeignKey('auth.User')
    finished_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'matches'

    def __unicode__(self):
        return "%s vs. %s" % (self.teamA.name, self.teamB.name)


class TeamResult(models.Model):
    team = models.ForeignKey(Team)

    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)

    goal_shot = models.IntegerField(default=0)
    goal_diff = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def __unicode__(self):
        return "{0} - {1} - {2} -> {3}".format(self.wins, self.draws,
                self.loses, self.team)


class Group(models.Model):
    name = models.CharField(max_length=200)
    teams = models.ManyToManyField(Team)
    matches = models.ManyToManyField(Match)
    results = models.ManyToManyField(TeamResult)

    def __unicode__(self):
        return self.name

    def sorted_results(self):
        return self.results.all().order_by('points', 'goal_diff').reverse()

    def sorted_matches(self):
        return self.matches.filter(playing='D').reverse()



class Competition(models.Model):
    name = models.CharField(max_length=200)
    groups = models.ManyToManyField(Group)

    def __unicode__(self):
        return self.name


class NewMatchForm(ModelForm):
    class Meta:
        model = Match
        fields = ['teamA', 'teamB', 'referee']

