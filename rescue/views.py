from django.shortcuts import render_to_response, get_object_or_404, redirect
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from dance.models import (Event, Competition, Group, Team, Performance,
        NewEventForm, NewTeamForm)
from django.core.context_processors import csrf
from django.contrib import messages
