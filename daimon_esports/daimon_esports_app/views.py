from rest_framework import generics
from .models import User, Discipline, Tournament, Roster, Game, Player, Request
from .serializers import UserSerializer, DisciplineSerializer, TournamentSerializer, RosterSerializer, GameSerializer, PlayerSerializer, RequestSerializer

# Create your views here.

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DisciplineList(generics.ListCreateAPIView):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer

class DisciplineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer

class TournamentList(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class TournamentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class RosterList(generics.ListCreateAPIView):
    queryset = Roster.objects.all()
    serializer_class = RosterSerializer

class RosterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Roster.objects.all()
    serializer_class = RosterSerializer

class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class RequestList(generics.ListCreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

class RequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer