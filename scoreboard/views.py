from django.shortcuts import render_to_response, get_object_or_404, redirect



@render_to('index.html')
def index(request):
    return {}
