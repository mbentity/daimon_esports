from django.contrib import admin

# Register your models here.

from .models import User, Discipline, Tournament, Roster, Game, Player, Request

admin.site.register(User)
admin.site.register(Discipline)
admin.site.register(Tournament)
admin.site.register(Roster)
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Request)