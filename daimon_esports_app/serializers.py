from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Discipline, Tournament, Team, Game, Player, Request

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'password', 'organizer']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'organizer': {'read_only': True},
        }
    def create(self, validated_data):
        user = User(
            name=validated_data['name'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        depth = 1

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
        depth = 1

class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    team1 = GameSerializer(many=True, read_only=True)
    team2 = GameSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = '__all__'
        depth = 1

class TournamentSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)
    games = GameSerializer(many=True, read_only=True)
    class Meta:
        model = Tournament
        fields = '__all__'
        depth = 1

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
        depth = 1

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'

class TournamentSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'
        depth = 1

class TournamentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        exclude = ['id']
    def create(self, validated_data):
        tournament = Tournament.objects.create(**validated_data)
        return tournament

class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['user', 'name', 'tag', 'tournament', 'logo']
    def create(self, validated_data):
        user = validated_data.get('user')
        team = Team.objects.create(**validated_data)
        Player.objects.create(user=user, team=team)
        return team