from django.shortcuts import render_to_response, get_object_or_404, redirect
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from models import (Event, Competition, Group, Team, Performance, NewEventForm, NewTeamForm)
from django.core.context_processors import csrf
from django.contrib import messages

@render_to('dance/index_dance.html')
def index_dance(request):
    events = Event.objects.all()
    return {'user': request.user, 'events': events}



# event/s
@render_to('dance/events.html')
@login_required(login_url='/login/')
def events(request):
    events = Event.objects.all()
    return {'events': events}

@render_to('dance/event.html')
@login_required(login_url='/login/')
def event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    competitions = event.competitions.all()
    return {'event': event, 'competitions': competitions}

@render_to('dance/event/new.html')
@login_required(login_url='/login/')
def new_event(request):
    if request.method == 'POST':
        form = NewEventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            event = Event(name=name)
            event.save()

            msg = "New event {0} has been created!".format(name)
            messages.success(request, msg)

            return redirect('index_dance')
    else:
        form = NewEventForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form
        return c

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

@render_to('dance/competition/new.html')
@login_required(login_url='/login/')
def new_competition(request):
    event = None
    if 'event' in request.GET:
        event = get_object_or_404(Event, pk=int(request.GET['event']))
    if request.method == 'POST':
        form = NewEventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            competition = Competition(name=name)
            competition.save()

            event.competitions.add(competition)
            event.save()

            msg = "New competition {0} has been created!".format(name)
            messages.success(request, msg)

            return redirect('dance.views.competition', str(competition.id))
    else:
        form = NewEventForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form
        if event:
            c['event'] = event
        else:
            c['events'] = Event.objects.all()
        return c

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

@render_to('dance/group/new.html')
@login_required(login_url='/login/')
def new_group(request):
    competition = None
    event = None
    if 'competition' in request.GET:
        competition = get_object_or_404(Competition, pk=int(request.GET['competition']))
        event = competition.event_set.all()[0]
    if request.method == 'POST':
        form = NewEventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            group = Group(name=name)
            group.save()

            competition.groups.add(group)
            competition.save()

            msg = "New group {0} has been created!".format(name)
            messages.success(request, msg)

            return redirect('dance.views.group', str(group.id))
    else:
        form = NewEventForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form

        if competition:
            c['competition'] = competition
        else:
            c['competitions'] = Competition.objects.all()

        if event:
            c['event'] = event
        else:
            c['events'] = Event.objects.all()
 
        return c

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

    performances = Performance.objects.filter(team=team).order_by('playing')
    performed = Performance.objects.filter(team=team, playing='D').count()

    return {'group': group, 'competition': competition, 'event': event,
            'team': team, 'performances': performances, 'performed': performed}

@render_to('dance/team/new.html')
@login_required(login_url='/login/')
def new_team(request):
    if 'group' in request.GET:
        group = get_object_or_404(Group, pk=int(request.GET['group']))
        competition = group.competition_set.all()[0]
        event = competition.event_set.all()[0]
    if request.method == 'POST':
        form = NewTeamForm(request.POST)
        if form.is_valid():
            teams = form.cleaned_data['names']
            teams = teams.replace('\r', "")
            teams = teams.split('\n')
            
            for t in teams:
                team = Team(name=t)
                team.save()
                group.teams.add(team)
            
            group.save()

            msg = "Teams for group {0} has been created!".format(group.name)
            messages.success(request, msg)

            return redirect('dance.views.group', str(group.id))
    else:
        form = NewTeamForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form
        c['group'] = group
        c['competition'] = competition
        c['event'] = event
        return c

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
