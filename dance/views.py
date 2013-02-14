from django.shortcuts import render_to_response, get_object_or_404, redirect
from annoying.decorators import render_to


@render_to('league_chooser.html')
def main_index(request):
    return {}
