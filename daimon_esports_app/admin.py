from django.contrib import admin
from django import forms

# Register your models here.

from .models import User, Discipline, Tournament, Team, Game, Player, Request

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['id', 'password']
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm

class DisciplineAdminForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = '__all__'
        exclude = ['id']
class DisciplineAdmin(admin.ModelAdmin):
    form = DisciplineAdminForm

class TournamentAdminForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = '__all__'
        exclude = ['id']
class TournamentAdmin(admin.ModelAdmin):
    form = TournamentAdminForm

class TeamAdminForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        exclude = ['id']
class TeamAdmin(admin.ModelAdmin):
    form = TeamAdminForm

class GameAdminForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'
        exclude = ['id']
class GameAdmin(admin.ModelAdmin):
    form = GameAdminForm

class PlayerAdminForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        exclude = ['id']
class PlayerAdmin(admin.ModelAdmin):
    form = PlayerAdminForm

class RequestAdminForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = '__all__'
        exclude = ['id']
class RequestAdmin(admin.ModelAdmin):
    form = RequestAdminForm

admin.site.register(User, UserAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Request, RequestAdmin)