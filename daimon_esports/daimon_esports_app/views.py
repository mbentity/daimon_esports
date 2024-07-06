from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User, Discipline, Tournament, Team, Game, Player, Request
from .serializers import RegisterSerializer, LogoutSerializer, UserSerializer, DisciplineSerializer, TournamentSerializer, TournamentSearchSerializer, TeamSerializer, GameSerializer, PlayerSerializer, RequestSerializer
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters
from django.utils import timezone

# Create your views here.

def index(request):
    return HttpResponse("Daimon Esports API", status=status.HTTP_200_OK)

class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user).data)
    def delete(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            request.user.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        return Response("User deleted", status=status.HTTP_200_OK)

class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class UserLogout(generics.CreateAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        return Response("Logged out", status=status.HTTP_200_OK)

class UserAuthenticated(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return HttpResponse("Authenticated", status=status.HTTP_200_OK)

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

class CompletedFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        completed = request.query_params.get('completed', None)
        if completed is not None:
            if completed.lower() == 'true':
                return queryset.filter(games_stop__lte=timezone.now())
            elif completed.lower() == 'false':
                return queryset.exclude(games_stop__lte=timezone.now())
        return queryset
    
class ClosedFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        closed = request.query_params.get('closed', None)
        if closed is not None:
            if closed.lower() == 'true':
                return queryset.filter(sub_stop__lte=timezone.now())
            elif closed.lower() == 'false':
                return queryset.exclude(sub_stop__lte=timezone.now())
        return queryset

class TournamentSearch(generics.ListAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSearchSerializer
    filter_backends = [filters.SearchFilter, CompletedFilter, ClosedFilter]
    search_fields = ['name', 'discipline__name']

class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GamePop(generics.ListAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        count = self.request.query_params.get('count', None)
        now = timezone.now()
        queryset = Game.objects.all()
        filtered_games = [
            game for game in queryset
            if game.timestamp >= now - timezone.timedelta(minutes=game.minutes)
        ]
        sorted_games = sorted(filtered_games, key=lambda game: game.timestamp)
        if count is not None:
            return sorted_games[:int(count)]
        return sorted_games[:5]

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