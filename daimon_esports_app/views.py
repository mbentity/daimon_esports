from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User, Discipline, Tournament, Team, Game, Player, Request
from .serializers import RegisterSerializer, LogoutSerializer, TeamCreateSerializer, TournamentCreateSerializer, UserPasswordSerializer, UserSerializer, DisciplineSerializer, TournamentSerializer, TournamentSearchSerializer, TeamSerializer, GameSerializer, PlayerSerializer, RequestSerializer
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

class UserName(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user).data)
    def post(self, request, *args, **kwargs):
        user = request.user
        user.name = request.data['name']
        user.save()
        return Response(self.serializer_class(user).data)

class UserUserName(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user).data)
    def post(self, request, *args, **kwargs):
        user = request.user
        user.username = request.data['username']
        user.save()
        return Response(self.serializer_class(user).data)

class UserPassword(generics.CreateAPIView):
    serializer_class = UserPasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response("Password changed", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class UserTournaments(generics.ListAPIView):
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Tournament.objects.filter(user=self.request.user)

class UserTeams(generics.ListAPIView):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        players = Player.objects.filter(user=self.request.user)
        if players.exists():
            teams = Team.objects.filter(players__in=players)
            if teams.exists():
                return teams
        return Team.objects.none()

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

class TournamentCanCreateTeam(generics.RetrieveAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = self.request.user
        tournament = self.get_object()
        isAlreadyInTournament = Player.objects.filter(user=user, team__tournament=tournament).exists()
        isTournamentOrganizer = tournament.user == user
        hasPendingRequests = Request.objects.filter(sender=user, team__tournament=tournament).exists()
        if isAlreadyInTournament or isTournamentOrganizer or hasPendingRequests:
            return Response(False)
        return Response(True)

class TournamentCreate(generics.CreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        # allow only if user is an organizer
        if not request.user.organizer:
            return Response("User is not an organizer", status=status.HTTP_403_FORBIDDEN)
        return Response(self.serializer_class(data=request.data).is_valid())

class TournamentUpdate(generics.UpdateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        if not request.user.organizer:
            return Response("User is not an organizer", status=status.HTTP_403_FORBIDDEN)
        tournament = self.get_object()
        if tournament.user != request.user:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        return self.update(request, *args, **kwargs)

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

class TeamCreate(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return self.create(request, *args, **kwargs)

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
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        request = self.get_object()
        user = self.request.user
        if request.sender == user or request.receiver == user:
            request.delete()
            return Response("Request deleted", status=status.HTTP_200_OK)
        return Response("User is not the sender or receiver", status=status.HTTP_403_FORBIDDEN)

class RequestCreate(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = self.request.user
        teamId = request.data['team']
        team = Team.objects.get(id=teamId)
        teamOwner = team.user
        object = Request(sender=user, receiver=teamOwner, team=team)
        object.save()
        return Response("Request sent", status=status.HTTP_200_OK)

class RequestAccept(generics.UpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        user = self.request.user
        request = self.get_object()
        if request.receiver == user:
            player = Player(user=request.sender, team=request.team)
            player.save()
            request.delete()
            Request.objects.filter(sender=request.sender, team__tournament=request.team.tournament).delete()
            return Response("Request accepted", status=status.HTTP_200_OK)
        return Response("User is not the receiver", status=status.HTTP_403_FORBIDDEN)

class UserRequests(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Request.objects.filter(receiver=user)

class UserOutgoingRequests(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Request.objects.filter(sender=user)