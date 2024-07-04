from rest_framework import serializers
from .models import User, Discipline, Tournament, Roster, Game, Player, Request

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['__all__']

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['__all__']

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['__all__']

class RosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roster
        fields = ['__all__']

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['__all__']

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['__all__']

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['__all__']