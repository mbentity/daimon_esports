from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User, Discipline, Tournament, Team, Game, Player, Request
from .serializers import TeamCreateSerializer, TournamentCreateSerializer, UserSerializer, UserSerializer, DisciplineSerializer, TournamentSerializer, TournamentSearchSerializer, TeamSerializer, GameSerializer, PlayerSerializer, RequestSerializer
from django.http import HttpResponse
from rest_framework import filters
from django.utils import timezone

def index(request):
    return HttpResponse("Daimon Esports API", status=status.HTTP_200_OK)

class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user).data)
    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response("User deleted", status=status.HTTP_200_OK)

class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.check_password(request.data['password']):
            return Response("Invalid password", status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data['newPassword'])
        user.save()
        return Response("Password changed", status=status.HTTP_200_OK)

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

class UserTournaments(generics.ListAPIView):
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Tournament.objects.filter(user=self.request.user)

class UserRequestsIn(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Request.objects.filter(receiver=user)

class UserRequestsOut(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Request.objects.filter(sender=user)

class DisciplineList(generics.ListCreateAPIView):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer

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

class DisciplineFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        discipline = request.query_params.get('discipline', None)
        if discipline is not None:
            return queryset.filter(discipline__id=discipline)
        return queryset

class TournamentSearch(generics.ListAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSearchSerializer
    filter_backends = [filters.SearchFilter, CompletedFilter, ClosedFilter, DisciplineFilter]
    search_fields = ['name', 'discipline__name']

class TournamentCreate(generics.CreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        if not request.user.organizer:
            return Response("User is not an organizer", status=status.HTTP_403_FORBIDDEN)
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TournamentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class TournamentName(generics.UpdateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        if not request.user.organizer:
            return Response("User is not an organizer", status=status.HTTP_403_FORBIDDEN)
        tournament = self.get_object()
        if tournament.user != request.user:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        tournament.name = request.data['name']
        tournament.save()
        return Response(self.serializer_class(tournament).data)
    
class TournamentDiscipline(generics.UpdateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        if not request.user.organizer:
            return Response("User is not an organizer", status=status.HTTP_403_FORBIDDEN)
        tournament = self.get_object()
        if tournament.user != request.user:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        tournament.discipline = Discipline.objects.get(id=request.data['discipline'])
        tournament.save()
        return Response(self.serializer_class(tournament).data)
    
class TournamentStream(generics.UpdateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        if not request.user.organizer:
            return Response("User is not an organizer", status=status.HTTP_403_FORBIDDEN)
        tournament = self.get_object()
        if tournament.user != request.user:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        tournament.streaming_platform = request.data['streamingPlatform']
        tournament.save()
        return Response(self.serializer_class(tournament).data)
    
class TournamentMeet(generics.UpdateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        if not request.user.organizer:
            return Response("User is not an organizer", status=status.HTTP_403_FORBIDDEN)
        tournament = self.get_object()
        if tournament.user != request.user:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        tournament.meeting_platform = request.data['meetingPlatform']
        tournament.save()
        return Response(self.serializer_class(tournament).data)

class TournamentDates(generics.UpdateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        if not request.user.organizer:
            return Response("User is not an organizer", status=status.HTTP_403_FORBIDDEN)
        tournament = self.get_object()
        if tournament.user != request.user:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        tournament.sub_start = request.data['subStart']
        tournament.sub_stop = request.data['subStop']
        tournament.games_start = request.data['gamesStart']
        tournament.games_stop = request.data['gamesStop']
        tournament.save()
        return Response(self.serializer_class(tournament).data)

class TournamentCanSubscribe(generics.RetrieveAPIView):
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
    def put(self, request, *args, **kwargs):
        team = self.get_object()
        user = self.request.user
        if team.user == user:
            team.name = request.data['name']
            team.save()
            return Response(self.serializer_class(team).data)
        return Response("User is not the team owner", status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, *args, **kwargs):
        team = self.get_object()
        user = self.request.user
        if team.user == user:
            team.delete()
            return Response("Team deleted", status=status.HTTP_200_OK)
        return Response("User is not the team owner", status=status.HTTP_403_FORBIDDEN)
    
class TeamTransferOwnership(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        team = self.get_object()
        user = self.request.user
        if team.user == user:
            newOwner = User.objects.get(id=request.data['newOwner'])
            team.user = newOwner
            team.save()
            return Response(self.serializer_class(team).data)
        return Response("User is not the team owner", status=status.HTTP_403_FORBIDDEN)
    
class TeamLogo(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        team = self.get_object()
        user = self.request.user
        if team.user == user:
            team.logo = request.data['logo']
            team.save()
            return Response(self.serializer_class(team).data)
        return Response("User is not the team owner", status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, *args, **kwargs):
        team = self.get_object()
        user = self.request.user
        if team.user == user:
            team.logo = None
            team.save()
            return Response(self.serializer_class(team).data)
        return Response("User is not the team owner", status=status.HTTP_403_FORBIDDEN)

class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GameTeams(generics.RetrieveUpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        game = self.get_object()
        user = self.request.user
        if game.tournament.user != user:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        game.team1 = Team.objects.get(id=request.data['team1'])
        game.team2 = Team.objects.get(id=request.data['team2'])
        game.save()
        return Response(self.serializer_class(game).data)
    
class GameScore(generics.UpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        game = self.get_object()
        game.score = request.data['score']
        game.save()
        return Response(self.serializer_class(game).data)
    
class GameTime(generics.UpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        game = self.get_object()
        game.time = request.data['time']
        game.save()
        return Response(self.serializer_class(game).data)
    
class GameMinutes(generics.UpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        game = self.get_object()
        game.minutes = request.data['minutes']
        game.save()
        return Response(self.serializer_class(game).data)

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        player = self.get_object()
        user = self.request.user
        # only the player or the team owner can delete the player
        if player.user == user or player.team.user == user:
            player.delete()
            return Response("Player deleted", status=status.HTTP_200_OK)
        return Response("User is not the player or the team owner", status=status.HTTP_403_FORBIDDEN)

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