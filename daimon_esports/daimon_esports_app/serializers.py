from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Discipline, Tournament, Team, Game, Player, Request

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['name', 'username', 'password']
    def create(self, validated_data):
        user = User(
            name=validated_data['name'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LogoutSerializer(serializers.Serializer):
    pass

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'password', 'organizer']
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class UserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'

class TournamentCreateSerializer(serializers.ModelSerializer):
    sub_start_timestamp = serializers.CharField(write_only=True)
    sub_stop_timestamp = serializers.CharField(write_only=True)
    games_start_timestamp = serializers.CharField(write_only=True)
    games_stop_timestamp = serializers.CharField(write_only=True)
    class Meta:
        model = Tournament
        fields = ['name', 'discipline', 'team_count', 'player_count', 'meeting_platform', 'streaming_platform',
                    'sub_start_timestamp', 'sub_stop_timestamp', 'games_start_timestamp', 'games_stop_timestamp']
    def create(self, validated_data):
        try:
            sub_start_timestamp = validated_data.pop('sub_start_timestamp')
            sub_stop_timestamp = validated_data.pop('sub_stop_timestamp')
            games_start_timestamp = validated_data.pop('games_start_timestamp')
            games_stop_timestamp = validated_data.pop('games_stop_timestamp')

            validated_data['sub_start'] = datetime.fromisoformat(sub_start_timestamp)
            validated_data['sub_stop'] = datetime.fromisoformat(sub_stop_timestamp)
            validated_data['games_start'] = datetime.fromisoformat(games_start_timestamp)
            validated_data['games_stop'] = datetime.fromisoformat(games_stop_timestamp)
            validated_data['user'] = self.context['request'].user

            return Tournament.objects.create(**validated_data)
        except OSError as e:
            raise serializers.ValidationError(f"Invalid timestamp: {e}")

class TournamentSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'
        depth = 1

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