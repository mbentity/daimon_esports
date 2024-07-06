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


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'

class TournamentSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'
        depth = 1

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        depth = 1

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'