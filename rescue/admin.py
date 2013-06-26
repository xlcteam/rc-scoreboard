from django.contrib import admin
from .models import Team, Group, Competition, Performance, SimpleRun, SimpleMap

admin.site.register(Team)
admin.site.register(Performance)
admin.site.register(Group)
admin.site.register(Competition)
admin.site.register(SimpleMap)
admin.site.register(SimpleRun)
