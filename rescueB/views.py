# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, redirect
from annoying.decorators import render_to
from rescueB.models import Team, SimpleMap, SimpleRun
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

@render_to('rescueB/index.html')
@login_required(login_url='/login/')
def index_rescueB(request):
    return {}

@render_to('rescueB/map/editor.html')
@login_required(login_url='/login/')
def mapeditor_view(request):
    return {}

@login_required(login_url='/login/')
@csrf_exempt
def mapeditor_save(request):
    data = json.loads(request.POST['json'])

    if data['action'] == 'getTiles':
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
