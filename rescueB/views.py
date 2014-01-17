from django.shortcuts import render_to_response, get_object_or_404, redirect
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from rescueB.models import (Competition, Group, Team, NewEventForm, Performance,
        NewTeamForm, MatchSaveForm, NewGroupForm)
from django.core.context_processors import csrf
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.template import Context, RequestContext
# from rescueB.helpers import *
from django.http import HttpResponse
import json

@render_to('rescueB/index_rescueB.html')
def index_rescueB(request):
    competitions = Competition.objects.all()
    return {'user': request.user, 'competitions': competitions}


# competition/s
@render_to('rescueB/competition.html')
@login_required(login_url='/login/')
def competition(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    groups = competition.groups.all()
    return {'competition': competition, 'groups': groups}

@render_to('rescueB/competitions.html')
@login_required(login_url='/login/')
def competitions(request):
    competitions = Competition.objects.all()
    return {'competitions': competitions}

@render_to('rescueB/competition/new.html')
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

            return redirect('rescueB.views.competition', str(competition.id))
    else:
        form = NewEventForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form
        return c

# group/s
@render_to('rescueB/group.html')
@login_required(login_url='/login/')
def group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    teams = group.teams.all()
    competition = group.competition_set.all()[0]
    performances = group.performances.all()

    if group.perfs_final:
        perfs_final = group.perfs_final.all()

    return {'group': group, 'teams': teams,
            'competition': competition,
            'performances': performances}

@render_to('rescueB/groups.html')
@login_required(login_url='/login/')
def groups(request):
    groups = Group.objects.all()
    return {'groups': groups}

@render_to('rescueB/group/new.html')
@login_required(login_url='/login/')
def new_group(request):
    competition = None
    if 'competition' in request.GET:
        competition = get_object_or_404(Competition, pk=int(request.GET['competition']))
    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            results_type = form.cleaned_data['results_type']

            group = Group(name=name, results_type=results_type,
                          map=form.cleaned_data['map'])
            group.save()

            competition.groups.add(group)
            competition.save()

            msg = "New group {0} has been created!".format(name)
            messages.success(request, msg)

            return redirect('rescueB.views.group', str(group.id))
    else:
        form = NewGroupForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form

        if competition:
            c['competition'] = competition
        else:
            c['competitions'] = Competition.objects.all()
 
        return c

# team/s
@render_to('rescueB/teams.html')
@login_required(login_url='/login/')
def teams(request):
    teams = Team.objects.all()
    return {'teams': teams}

@render_to('rescueB/team.html')
@login_required(login_url='/login/')
def team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    group = team.group_set.all()[0]
    competition = group.competition_set.all()[0]

    performances = Performance.objects.filter(team=team).order_by('playing')
    performed = Performance.objects.filter(team=team, playing='D').count()

    return {'group': group, 'competition': competition,
            'team': team, 'performances': performances, 'performed': performed}

@render_to('rescueB/team/new.html')
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

            return redirect('rescueB.views.group', str(group.id))
    else:
        form = NewTeamForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form
        c['group'] = group
        c['competition'] = competition
        return c

#results
@render_to('rescueB/results/live.html')
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
        return {'competitions': Competition.objects.all()}

@render_to('rescueB/performances/generate.html')
@login_required(login_url='/login/')
def performances_generate(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    competition = group.competition_set.all()[0]

    return {'group': group, 'competition': competition}

@render_to('rescueB/performances/generate_listing.html')
def performances_generate_listing(request):
    group = get_object_or_404(Group, pk=request.POST['group_id'])
    teams = list(group.teams.all())

    n_rounds = 3
    if group.results_type == 'D':
        n_rounds = 2

    for rnd in range(1, 1+n_rounds):
        for team in teams:
            performance = Performance(team=team, round_number=rnd, referee=request.user)
            performance.save()
            group.performances.add(performance)
       
    group.save()
    performances = group.performances.all().order_by('round_number')
    return {'performances': performances, 'group': group}

@login_required(login_url='/login/')
@csrf_exempt
def performance_play(request, performance_id):
    performance = get_object_or_404(Performance, pk=performance_id)
       
    return render_to_response('rescueB/performances/play.html',
                              {'performance': performance, 'performance_id': performance_id},
                              context_instance=RequestContext(request))

@render_to('rescueB/performances/save.html')
@login_required(login_url='/login/')
def performance_save(request, performance_id):
    scoresheet = {  
          'floating_victim' : 25,
          'linear_victim': 10,
          'false_victim' : -10,
          'successful_exit': 10,
    }    

    def errorHandle(error, request, performance_id):
        post = request.POST
        initial = {'floating_victim': post["floating_victim"], 'linear_victim': post["linear_victim"],
                   'false_victim': post["false_victim"], 'lack_of_progress': post["lack_of_progress"],
                   'successful_exit': post["successful_exit"], 'reliability': post['reliability'], 
                   'time': post["time"], 'points': post["points"],}

        for x in scoresheet:
            if post[x] == u'---' or post[x] == '---':
                initial[x] = "0"
            else:            
                initial[x] = post[x]

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
                
                performance.floating_victim = scoresheet["floating_victim"] * int(request.POST["floating_victim"])
                performance.linear_victim = scoresheet["linear_victim"] * int(request.POST["linear_victim"])
                performance.false_victim = scoresheet["false_victim"] * int(request.POST["false_victim"])
                performance.successful_exit = scoresheet["successful_exit"] * int(request.POST["successful_exit"])

                performance.lack_of_progress = scoresheet["lack_of_progress"]

                performance.reliability = int(request.POST["reliability"])
                performance.points = int(request.POST["points"])
                
                strtime = request.POST["time"]
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
                return redirect('rescueB.views.index_rescueB')
            else:
                return res
        else:
            form = MatchSaveForm(request.POST)
            if form.is_valid(): 
                res = authorize_and_save(request)
                if res is True:
                    return redirect('rescueB.views.index_rescueB')
                else:
                    return res
            else:
                return errorHandle('Invalid login', request, performance_id)
    else:
        return {'error': "How on earth did you get here?"}

@login_required(login_url='/login/')
def table_final_generate(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    for team in group.teams.all():
        teamres = group.performances.filter(team=team).order_by('points', 'time').reverse()   
        if group.results_type == 'S':

            newperf = Performance(team=team, round_number=4)
            newperf.referee = request.user
            newperf.room1 = teamres[0].room1 + teamres[1].room1
            newperf.room2 = teamres[0].room2 + teamres[1].room2
            newperf.room3 = teamres[0].room3 + teamres[1].room3
            newperf.ramp = teamres[0].ramp + teamres[1].ramp
            newperf.hallway = teamres[0].hallway + teamres[1].hallway
            newperf.gap = teamres[0].gap + teamres[1].gap
            newperf.obstacle = teamres[0].obstacle + teamres[1].obstacle
            newperf.speed_bump = teamres[0].speed_bump + teamres[1].speed_bump
            newperf.intersection = teamres[0].intersection + teamres[1].intersection
            newperf.victim = teamres[0].victim + teamres[1].victim
            newperf.lift = teamres[0].lift + teamres[1].lift

            newperf.points = teamres[0].points + teamres[1].points
            newperf.time = teamres[0].time + teamres[1].time

            newperf.save()
        else:
            newperf = teamres[0]

        group.perfs_final.add(newperf)

    group.result_table_generated = True
    group.save()
    return redirect('rescueB.views.group', group_id)


@login_required(login_url='/login/')
def results_group_pdf(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    competition = group.competition_set.all()[0]
    performances = group.performances.all()

    return render_to_pdf(request, 'rescueB/results/generate/group.html',
                            {'competition': competition, 'group': group,
                             'performances': performances, 'title': group.name})

@render_to('rescueB/results/performance.html')
@login_required(login_url='/login/')
def results_performance_view(request, performance_id):
    performance = get_object_or_404(Performance, pk=performance_id)

    group = performance.group_set.all()[0]
    competition = group.competition_set.all()[0]
    return {'group': group, 'performance': performance,
            'competition': competition}










@render_to('rescueB/map/editor.html')
@login_required(login_url='/login/')
def mapeditor_view(request):
    return {}

@login_required(login_url='/login/')
@csrf_exempt
def mapeditor_save(request):
    data = json.loads(request.POST['json'])

    if data['action'] == 'getMaze':
        id = data['mapID']
        map = get_object_or_404(SimpleMap, pk=id)
        return HttpResponse(map.data,
                mimetype="application/json")


    if data['mapID'] == -1: 
        name = data['name']
        map = SimpleMap(name=name, data='')
        map.save()
        data['mapID'] = map.id
        map.data = json.dumps(data)
        map.save()

        messages.success(request, "The map has been saved");
        return HttpResponse(json.dumps(map.id),
                mimetype="application/json")
    else:
        map = get_object_or_404(SimpleMap, pk=data['mapID'])
        map.data = request.POST['json']
        map.save()
        return HttpResponse(json.dumps(map.id),
                mimetype="application/json")

    return {}

@render_to('rescueB/map/editor.html')
@login_required(login_url='/login/')
def mapeditor_edit(request, map_id):
    return {'id': map_id}

@render_to('rescueB/map/listing.html')
@login_required(login_url='/login/')
def mapeditor_listing(request):
    maps = SimpleMap.objects.all()
    return {'maps': maps}
