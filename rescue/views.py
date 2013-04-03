from django.shortcuts import render_to_response, get_object_or_404, redirect
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from rescue.models import (Competition, Group, Team, NewEventForm, Performance,
        NewTeamForm, MatchSaveForm)
from django.core.context_processors import csrf
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.template import Context, RequestContext

@render_to('rescue/index_rescue.html')
def index_rescue(request):
    competitions = Competition.objects.all()
    return {'user': request.user, 'competitions': competitions}


# competition/s
@render_to('rescue/competition.html')
@login_required(login_url='/login/')
def competition(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    groups = competition.groups.all()
    return {'competition': competition, 'groups': groups}

@render_to('rescue/competitions.html')
@login_required(login_url='/login/')
def competitions(request):
    competitions = Competition.objects.all()
    return {'competitions': competitions}

@render_to('rescue/competition/new.html')
@login_required(login_url='/login/')
def new_competition(request):
    if request.method == 'POST':
        form = NewEventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            competition = Competition(name=name)
            competition.save()

            msg = "New competition {0} has been created!".format(name)
            messages.success(request, msg)

            return redirect('rescue.views.competition', str(competition.id))
    else:
        form = NewEventForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form
        return c

# group/s
@render_to('rescue/group.html')
@login_required(login_url='/login/')
def group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    teams = group.teams.all()
    competition = group.competition_set.all()[0]
    performances = group.performances.all()

    return {'group': group, 'teams': teams,
            'competition': competition,
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
    if 'competition' in request.GET:
        competition = get_object_or_404(Competition, pk=int(request.GET['competition']))
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

    performances = Performance.objects.filter(team=team).order_by('playing')
    performed = Performance.objects.filter(team=team, playing='D').count()

    return {'group': group, 'competition': competition,
            'team': team, 'performances': performances, 'performed': performed}

@render_to('rescue/team/new.html')
@login_required(login_url='/login/')
def new_team(request):
    if 'group' in request.GET:
        group = get_object_or_404(Group, pk=int(request.GET['group']))
        competition = group.competition_set.all()[0]
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
        return c

#results
@render_to('rescue/results/live.html')
def results_live(request):
    if 'competition' in request.GET:
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

    for rnd in range(1, 4):
        for team in teams:
            performance = Performance(team=team, round_number=rnd, referee=request.user)
            performance.save()
            group.performances.add(performance)
       
    group.save()
    performances = group.performances.all().order_by('round_number')
    return {'performances': performances}

@login_required(login_url='/login/')
@csrf_exempt
def performance_play(request, performance_id):
    performance = get_object_or_404(Performance, pk=performance_id)
       
    return render_to_response('rescue/performances/play.html',
                              {'performance': performance, 'performance_id': performance_id},
                              context_instance=RequestContext(request))

@render_to('rescue/performances/save.html')
@login_required(login_url='/login/')
def performance_save(request, performance_id):
    scoresheet = {
        'try' : {
            'room1' : {1 : 60, 2 : 40, 3 : 20},
            'room2' : {1 : 60, 2 : 40, 3 : 20},
            'room3' : {1 : 60, 2 : 40, 3 : 20},
            'ramp'  : {1 : 30, 2 : 20, 3 : 10},
            'hallway':{1 : 30, 2 : 20, 3 : 10},
            'victim': {1 : 60, 2 : 40, 3 : 20},      
        },
        'each' : {
            'gap' : 10,
            'obstacle': 10,
            'speed_bump': 5,
            'intersection': 10,
        }
    }    

    def errorHandle(error, request, performance_id):
        post = request.POST
        initial = {'gap': post["gap"], 'obstacle': post["obstacle"],
                        'speed_bump': post["speed_bump"], 'intersection': post["intersection"],
                        'time': post["time_dialog"], 'points': post["points_dialog"],}

        for x in scoresheet["try"]:
            
            if post[x] == u'---':
                initial[x] = u'4'
            else:            
                initial[x] = post[x]

        print initial
        form = MatchSaveForm(post, initial=initial)
        c = {}
        c.update(csrf(request))
        c['form'] = form
        c['error'] = error
        c['performance_id'] = performance_id
        return c
    
    def authorize_and_save(request):
        username = request.user
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                performance = get_object_or_404(Performance, pk=performance_id)
                performance.referee = request.user
                performance.playing = 'D'
                
                performance.room1 = scoresheet["try"]["room1"][int(request.POST["room1"])]
                performance.room2 = scoresheet["try"]["room2"][int(request.POST["room2"])]
                performance.room3 = scoresheet["try"]["room3"][int(request.POST["room3"])]
                performance.ramp = scoresheet["try"]["ramp"][int(request.POST["ramp"])]
                performance.hallway = scoresheet["try"]["hallway"][int(request.POST["hallway"])]
                performance.victim = scoresheet["try"]["victim"][int(request.POST["victim"])]                
                
                performance.gap = scoresheet["each"]["gap"] * int(request.POST["gap"])
                performance.obstacle = scoresheet["each"]["obstacle"] * int(request.POST["obstacle"])
                performance.speed_bump = scoresheet["each"]["speed_bump"] * int(request.POST["speed_bump"])
                performance.intersection = scoresheet["each"]["intersection"] * int(request.POST["intersection"])

                performance.points = int(request.POST["points_dialog"])
                
                strtime = request.POST["time_dialog"]
                finaltime = 0.0
                finaltime += float(strtime.split(':')[0]) * 60.0 
                finaltime += float(strtime.split(':')[1].replace(",", "."))
                performance.time = finaltime                

                performance.save()
                messages.success(request, "Performance of team {0} has been successfully saved"\
                                        .format(performance.team.name))

                return True
        return errorHandle('Invalid login', request, performance_id)

    
    if request.method == 'POST':
        if 'final' in request.POST:
            res = authorize_and_save(request)
            if res is True:
                return redirect('rescue.views.index_rescue')
            else:
                return res
        else:
            form = MatchSaveForm(request.POST)
            if form.is_valid(): 
                res = authorize_and_save(request)
                if res is True:
                    return redirect('rescue.views.index_rescue')
                else:
                    return res
            else:
                return errorHandle('Invalid login', request, performance_id)
    else:
        return {'error': "How on earth did you get here?"}
