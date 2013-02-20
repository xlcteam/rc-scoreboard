from django.shortcuts import render_to_response, get_object_or_404, redirect
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from .models import (Event, Competition, Group, Team)

@render_to('dance/index_dance.html')
def index_dance(request):
    return {}



# event/s
@render_to('dance/events.html')
@login_required(login_url='/login/')
def events(request):
    events = Event.objects.all()
    return {'events': events}

render_to('dance/event.html')
@login_required(login_url='/login/')
def event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    competitions = event.competitions.all()
    return {'event': event, 'competitions': competitions}

@render_to('dance/event/new.html')
@login_required(login_url='/login/')
def new_event(request):
    return {}

# competition/s
@render_to('dance/competition.html')
@login_required(login_url='/login/')
def competition(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    groups = competition.groups.all()
    event = competition.event_set.all()[0]
    return {'event': event, 'competition': competition, 'groups': groups}

@render_to('dance/competitions.html')
@login_required(login_url='/login/')
def competitions(request):
    competitions = Competition.objects.all()
    return {'competitions': competitions}

# group/s
@render_to('dance/group.html')
@login_required(login_url='/login/')
def group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    teams = group.teams.all()
    competition = group.competition_set.all()[0]
    event = competition.event_set.all()[0]

    return {'group': group, 'teams': teams,
            'competition': competition, 'event': event}

@render_to('dance/groups.html')
@login_required(login_url='/login/')
def groups(request):
    groups = Group.objects.all()
    return {'groups': groups}

# team/s
@render_to('dance/teams.html')
@login_required(login_url='/login/')
def teams(request):
    teams = Team.objects.all()
    return {'teams': teams}

@render_to('dance/team.html')
@login_required(login_url='/login/')
def team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    group = team.group_set.all()[0]
    competition = group.competition_set.all()[0]
    event = competition.event_set.all()[0]

    return {'group': group, 'competition': competition, 'event': event,
            'team': team}

#results
@render_to('dance/results/live.html')
def results_live(request):
    if 'event' in request.GET:
        event = get_object_or_404(Event, pk=request.GET['event'])
        return {'event': event, 'event_only': True}

    elif 'competition' in request.GET:
        competition = get_object_or_404(Competition, pk=request.GET['competition'])
        event = competition.event_set.all()[0]
        return {'event': event, 'competition': competition,
                'competition_only': True}

    elif 'group' in request.GET:
        group = get_object_or_404(Group, pk=request.GET['group'])
        competition = group.competition_set.all()[0]
        event = competition.event_set.all()[0]
        return {'event': event, 'competition': competition,
                'group': group, 'group_only': True}

    else:
        return {'events': Event.objects.all()}
