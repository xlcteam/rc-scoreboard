from django.shortcuts import render_to_response, get_object_or_404, redirect
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from rescue.models import (Event, Competition, Group, Team, Performance,
        NewEventForm, NewTeamForm)
from django.core.context_processors import csrf
from django.contrib import messages

@render_to('rescue/index_rescue.html')
def index_rescue(request):
    events = Event.objects.all()
    return {'user': request.user, 'events': events}



# event/s
@render_to('rescue/events.html')
@login_required(login_url='/login/')
def events(request):
    events = Event.objects.all()
    return {'events': events}

@render_to('rescue/event.html')
@login_required(login_url='/login/')
def event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    competitions = event.competitions.all()
    return {'event': event, 'competitions': competitions}

@render_to('rescue/event/new.html')
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

            return redirect('index_rescue')
    else:
        form = NewEventForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form
        return c

# competition/s
@render_to('rescue/competition.html')
@login_required(login_url='/login/')
def competition(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    groups = competition.groups.all()
    event = competition.event_set.all()[0]
    return {'event': event, 'competition': competition, 'groups': groups}

@render_to('rescue/competitions.html')
@login_required(login_url='/login/')
def competitions(request):
    competitions = Competition.objects.all()
    return {'competitions': competitions}

@render_to('rescue/competition/new.html')
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

            return redirect('rescue.views.competition', str(competition.id))
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
@render_to('rescue/group.html')
@login_required(login_url='/login/')
def group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    teams = group.teams.all()
    competition = group.competition_set.all()[0]
    event = competition.event_set.all()[0]
    performances = group.performances.all()

    return {'group': group, 'teams': teams,
            'competition': competition, 'event': event,
            'performances': performances}

@render_to('rescue/groups.html')
@login_required(login_url='/login/')
def groups(request):
    groups = Group.objects.all()
    return {'groups': groups}

@render_to('rescue/group/new.html')
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

            return redirect('rescue.views.group', str(group.id))
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
@render_to('rescue/teams.html')
@login_required(login_url='/login/')
def teams(request):
    teams = Team.objects.all()
    return {'teams': teams}

@render_to('rescue/team.html')
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

@render_to('rescue/team/new.html')
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

            return redirect('rescue.views.group', str(group.id))
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
@render_to('rescue/results/live.html')
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

@render_to('rescue/performances/generate.html')
@login_required(login_url='/login/')
def performances_generate(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    competition = group.competition_set.all()[0]

    return {'group': group, 'competition': competition}

@render_to('rescue/performances/generate_listing.html')
def performances_generate_listing(request):
    group = get_object_or_404(Group, pk=request.POST['group_id'])
    teams = list(group.teams.all())

    for team in teams:
        performance = Performance(team=team) #referee=request.user)
        performance.save()
        group.performances.add(performance)
    
    performances = group.performances.all()
    return {'performances': performances}

