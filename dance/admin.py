from django.contrib import admin
from .models import Team, Group, Competition, Performance, Event

admin.site.register(Team)
admin.site.register(Group)
admin.site.register(Competition)
admin.site.register(Event)
admin.site.register(Performance)
