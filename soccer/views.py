# Create your views here.
from django.shortcuts import (render_to_response, get_object_or_404, redirect,
            render)
from soccer.models import (Team, Group, Competition, Match,
        TeamResult, MatchSaveForm, NewEventForm, NewTeamForm, NewMatchForm)
from django.contrib.auth import authenticate
from django.core.context_processors import csrf
from django.template import Context, RequestContext
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib import messages
from soccer.helpers import *

@render_to('soccer/results_live.html')
def results_live(request):
    groups = Group.objects.all()
    return {'groups': groups, 'event': events}

@render_to('soccer/competition/new.html')
@login_required(login_url='/login/')
def new_competition(request):
    event = None
    if request.method == 'POST':
        form = NewEventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            competition = Competition(name=name)
            competition.save()

            msg = "New competition {0} has been created!".format(name)
            messages.success(request, msg)

            return redirect('soccer.views.competition', str(competition.id))
    else:
        form = NewEventForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form
        return c

@render_to('soccer/group/new.html')
@login_required(login_url='/login/')
def new_group(request):
    competition = None
    if 'competition' in request.GET:
        competition = get_object_or_404(Competition, pk=int(request.GET['competition']))
    if 'competition' in request.POST:
        competition = get_object_or_404(Competition, pk=int(request.POST['competition']))
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

            return redirect('soccer.views.group', str(group.id))
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

@render_to('soccer/team/new.html')
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

                result = TeamResult(team=team)

                group.teams.add(team)
                group.results.add(result)
            
            group.save()

            msg = "Teams for group {0} has been created!".format(group.name)
            messages.success(request, msg)

            return redirect('soccer.views.group', str(group.id))
    else:
        form = NewTeamForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form
        c['group'] = group
        c['competition'] = competition
        return c


@render_to('soccer/matches/new.html')
@login_required(login_url='/login/')
def new_match(request):
    if 'group' in request.GET:
        group = get_object_or_404(Group, pk=int(request.GET['group']))
        competition = group.competition_set.all()[0]
    if request.method == 'POST':
        form = NewMatchForm(request.POST)
        if form.is_valid():

            teamA = form.cleaned_data['teamA']
            teamB = form.cleaned_data['teamB']
            referee = form.cleaned_data['referee']

            match = Match(teamA=teamA, teamB=teamB, referee=referee)
            match.save()

            group.matches.add(match)

            msg = "The match between {1} and {2} in group {0} has been created!"\
                    .format(group.name, teamA, teamB)
            messages.success(request, msg)

            return redirect('soccer.views.group', str(group.id))
    else:
        form = NewMatchForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form
        c['group'] = group
        return c


# competition/s
@render_to('soccer/competition.html')
@login_required(login_url='/login/')
def competition(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    groups = competition.groups.all()
    return {'competition': competition, 'groups': groups}

@render_to('soccer/competitions.html')
@login_required(login_url='/login/')
def competitions(request):
    competitions = Competition.objects.all()
    return {'competitions': competitions}

# group/s
@render_to('soccer/group.html')
@login_required(login_url='/login/')
def group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    teams = group.teams.all()
    competition = group.competition_set.all()[0]
    team_results = group.results.all()\
                    .order_by('points').reverse()
    matches = group.matches.all().order_by('playing')
    return {'group': group, 'teams': teams,
            'competition': competition, 
            'matches': matches,
            'team_results': team_results}

@render_to('soccer/groups.html')
@login_required(login_url='/login/')
def groups(request):
    groups = Group.objects.all()
    return {'groups': groups}

# team/s
@render_to('soccer/teams.html')
@login_required(login_url='/login/')
def teams(request):
    teams = Team.objects.all()
    return {'teams': teams}

@render_to('soccer/team.html')
@login_required(login_url='/login/')
def team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    group = team.group_set.all()[0]
    competition = group.competition_set.all()[0]
    from itertools import chain

    matches = list(chain(Match.objects.filter(teamA=team).order_by('playing'),
            Match.objects.filter(teamB=team).order_by('playing')))
    played = Match.objects.filter(teamA=team, playing='D').count() + \
            Match.objects.filter(teamB=team, playing='D').count()

    return {'group': group, 'competition': competition,
            'team': team, 'matches': matches, 'played': played}

@render_to('soccer/index_soccer.html')
def index_soccer(request):
    matches = Match.objects.all()
    competitions = Competition.objects.all()
    return {'user': request.user, 'competitions': competitions, 'matches': matches}

@render_to('soccer/matches/generate.html')
@login_required(login_url='/login/')
def matches_generate(request, group_id=None):
    group = get_object_or_404(Group, pk=group_id)
    competition = group.competition_set.all()[0]
    return {'group': group, 'competition': competition}

@render_to('soccer/matches/generate_listing.html')
def matches_generate_listing(request):
    group = get_object_or_404(Group, pk=request.POST['group_id'])
    teams = list(group.teams.all())

    for team in teams:
        result = TeamResult(team=team)
        result.save()
        group.results.add(result)

    matches = []
    schedule = round_robin(teams)
    for round in schedule:
        for teams in round:
            match = Match(teamA=teams[0], teamB=teams[1], referee=request.user)
            match.save()
            group.matches.add(match)
            matches.append(match)
    return {'matches': matches, 'group': group}


@login_required(login_url='/login/')
@csrf_exempt
def match_play(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.POST:
        scoreA = request.POST.get('scoreA', None)
        scoreB = request.POST.get('scoreB', None)
        if scoreA and scoreB:
            match.scoreA = int(scoreA)
            match.scoreB = int(scoreB)
            match.playing = 'P'

            match.save()

        return HttpResponse('{ok: true}', mimetype="application/json") 
       
    return render_to_response('soccer/matches/play.html',
                              {'match': match, 'match_id': match_id},
                              context_instance=RequestContext(request))

@render_to('soccer/matches/save.html')
@login_required(login_url='/login/')
def match_save(request, match_id):
    
    def errorHandle(error, request, scoreA, scoreB, match_id):
        form = MatchSaveForm(request.POST, initial={'scoreA': scoreA, 'scoreB': scoreB})
        c = {}
        c.update(csrf(request))
        c['form'] = form
        c['error'] = error
        c['match_id'] = match_id
        return c
    
    def authorize_and_save(request):
        username = request.user
        password = request.POST['password']
        scoreA = request.POST['scoreA']
        scoreB = request.POST['scoreB']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                match = get_object_or_404(Match, pk=match_id)
                match.scoreA = scoreA
                match.scoreB = scoreB
                match.playing = 'D'
                match.save()

                rA = get_object_or_404(TeamResult, pk=match.teamA.id)
                rB = get_object_or_404(TeamResult, pk=match.teamB.id)

                if match.scoreA > match.scoreB:
                    rA.wins += 1
                    rA.points += 3
                    rB.loses += 1
                elif match.scoreB > match.scoreA:
                    rB.wins += 1
                    rB.points += 3
                    rA.loses += 1
                else:
                    rA.draws += 1
                    rB.draws += 1
                    rA.points += 1
                    rB.points += 1

                rA.matches_played += 1
                rB.matches_played += 1

                rA.goal_shot += int(match.scoreA)
                rB.goal_shot += int(match.scoreB)
                
                rA.goal_diff += int(match.scoreA) - int(match.scoreB)
                rB.goal_diff += int(match.scoreB) - int(match.scoreA)

                rA.save()
                rB.save()

                messages.success(request, "Match between {0} and {1}"
                                            " has been successfully saved"\
                                        .format(match.teamA.name, match.teamB.name))

                return True
        return errorHandle('Invalid login', request, scoreA, scoreB, match_id)

    if request.method == 'POST':
        if 'final' in request.POST:
            res = authorize_and_save(request)
            if res is True:
                return redirect('index')
            else:
                return res
        else:
            form = MatchSaveForm(request.POST)
            if form.is_valid(): 
                res = authorize_and_save(request)
                if res is True:
                    return redirect('index')
                else:
                    return res
            else:
                return errorHandle(u'Invalid login')
    else:
        return {'error': "How on earth did you get here?"}

@render_to('soccer/results/live.html')
def results_live(request):
    if 'competition' in request.GET:
        competition = get_object_or_404(Competition, pk=request.GET['competition'])
        return {'competition': competition,
                'competition_only': True}

    elif 'group' in request.GET:
        group = get_object_or_404(Group, pk=request.GET['group'])
        competition = group.competition_set.all()[0]
        return {'competition': competition,
                'group': group, 'group_only': True}

    else:
        return {'competitions': Competition.objects.all(), 
                'matches': Match.objects.filter(playing='P')}

@render_to('soccer/results/livefeed.html')
def results_live_feed(request):
    return {'matches': Match.objects.filter(playing='P')}

@render_to('soccer/results/livetables.html')
def results_live_tables(request):
    return {'competitions': Competition.objects.all()}



def results(request):
    pass

def results_team_view(request, team_id):
    pass

@render_to('soccer/results/group.html')
@login_required(login_url='/login/')
def results_group_view(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    teams = group.teams.all()
    competition = group.competition_set.all()[0]
    team_results = TeamResult.objects.filter(group__id=group.id)
    return {'group': group, 'teams': teams,
            'competition': competition,
            'team_results': team_results}

@render_to('soccer/results/match.html')
@login_required(login_url='/login/')
def results_match_view(request, match_id):
    match = get_object_or_404(Match, pk=match_id)

    group = match.group_set.all()[0]
    competition = group.competition_set.all()[0]
    return {'group': group, 'match': match,
            'competition': competition}

@login_required(login_url='/login/')
def results_group_pdf(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    competition = group.competition_set.all()[0]

    team_results = group.results.all()\
                    .order_by('points').reverse()
    matches = group.matches.filter(playing='D')

    return render_to_pdf(request, 'soccer/results/generate/group.html', 
                            {'competition': competition,
                             'group': group, 'team_results': team_results,
                             'matches': matches})

@login_required(login_url='/login/')
def results_competition_pdf(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    groups = competition.groups.all()

    return render_to_pdf(request, 'soccer/results/generate/competition.html', 
                            {'competition': competition,
                             'groups': groups})

@login_required(login_url='/login/')
def results_event_pdf(request, event_id):
    competitions = event.competitions.all()

    return render_to_pdf(request, 'soccer/results/generate/event.html', 
                            {'competitions': competitions})

def schedule_generate(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    competition = group.competition_set.all()[0]

    matches = group.matches.all()
    
    return render_to_pdf(request, 'soccer/results/generate/schedule.html',
                            {'competition': competition, 'matches': matches, 'group': group})


@render_to('soccer/results/livegroup.html')
@login_required(login_url='/login/')
def group_live_result(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    #match = group.matches.filter(playing='P')

    return {'group': group}


@login_required(login_url='/login/')
def group_live_json_result(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    matches = group.matches.filter(playing='P')
    if (len(matches) > 0):
        match = matches[0]

        out = '"teamA": "{0}", "teamB": "{1}", "scoreA": {2}, "scoreB": {3}'
        out = out.format(match.teamA.name, match.teamB.name, match.scoreA, match.scoreB)
        out = '{' + out + '}'

        return HttpResponse(out, mimetype="application/json")
    else:
        return HttpResponse('{"status": "No match is being played at the moment"}', 
                    mimetype="application/json") 

    
