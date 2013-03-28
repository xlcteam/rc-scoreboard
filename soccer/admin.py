from django.contrib import admin
from soccer.models import Team, Group, Competition, Match, TeamResult

admin.site.register(Team)
admin.site.register(Group)
admin.site.register(Competition)
admin.site.register(Match)
admin.site.register(TeamResult)
