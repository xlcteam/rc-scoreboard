from django.shortcuts import render_to_response, get_object_or_404, redirect
from annoying.decorators import render_to



@render_to('index.html')
def index(request):
    return {}
