from django.db import models
from django import forms

class NewEventForm(forms.Form):
    name = forms.CharField(max_length=30)

class NewGroupForm(forms.Form):
    name = forms.CharField(max_length=30)

    RESULTS_CHOICES = (
        ('S', 'Play three rounds - take the sum of the best two as the result (slovak system)'),
        ('D', 'Play two rounds - take the best one as the result (dutch system)'),
    )

    results_type = forms.ChoiceField(choices=RESULTS_CHOICES)

class NewTeamForm(forms.Form):
    names = forms.CharField(widget=forms.Textarea(attrs={'size':'20'}))

class MatchSaveForm(forms.Form):
    room1 = forms.IntegerField(label='Room 1 (try)')
    room2 = forms.IntegerField(label='Room 2 (try)')
    room3 = forms.IntegerField(label='Room 3 (try)')
    ramp = forms.IntegerField(label='Ramp (try)')
    hallway = forms.IntegerField(label='Hallway (try)')
    victim = forms.IntegerField(label='Victim (try)')
    gap = forms.IntegerField(label='Gap')
    obstacle = forms.IntegerField(label='Obstacle')
    speed_bump = forms.IntegerField(label='Speed Bump')
    intersection = forms.IntegerField(label='Intersection')
    lift = forms.IntegerField(label="Lift (secondary)")
    points = forms.IntegerField(label='Points')
    time = forms.CharField(label='Time')
    
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                max_length=100)

