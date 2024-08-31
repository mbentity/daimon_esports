from datetime import datetime
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User, Discipline, Tournament, Team, Game, Player, Request
from .serializers import UserSerializer, UserSerializer, DisciplineSerializer, TournamentReadSerializer, TournamentSerializer, TournamentSearchSerializer, TeamReadSerializer, TeamSerializer, GameReadSerializer, GameSerializer, PlayerSerializer, RequestSerializer
from django.http import HttpResponse
from rest_framework import filters
from django.utils import timezone
from PIL import Image

def index(request):
    return HttpResponse("Daimon Esports API", status=status.HTTP_200_OK)

class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response(self.serializer_class(user).data)
    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response("User deleted", status=status.HTTP_200_OK)

class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        name = request.data['name']
        isNameTaken = User.objects.filter(name=name).exists()
        if isNameTaken:
            return Response("Name already taken", status=status.HTTP_400_BAD_REQUEST)
        isNameTooShort = len(name) < 3
        if isNameTooShort:
            return Response("Name too short", status=status.HTTP_400_BAD_REQUEST)
        isNameTooLong = len(name) > 30
        if isNameTooLong:
            return Response("Name too long", status=status.HTTP_400_BAD_REQUEST)
        username = request.data['username']
        isUsernameTaken = User.objects.filter(username=username).exists()
        if isUsernameTaken:
            return Response("Username already taken", status=status.HTTP_400_BAD_REQUEST)
        isUsernameTooShort = len(username) < 3
        if isUsernameTooShort:
            return Response("Username too short", status=status.HTTP_400_BAD_REQUEST)
        isUsernameTooLong = len(username) > 30
        if isUsernameTooLong:
            return Response("Username too long", status=status.HTTP_400_BAD_REQUEST)
        password = request.data['password']
        isPasswordTooShort = len(password) < 3
        if isPasswordTooShort:
            return Response("Password too short", status=status.HTTP_400_BAD_REQUEST)
        isPasswordTooLong = len(password) > 30
        if isPasswordTooLong:
            return Response("Password too long", status=status.HTTP_400_BAD_REQUEST)
        return self.create(request, *args, **kwargs)

class UserName(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        name = request.data['name']
        isNameTaken = User.objects.filter(name=name).exists()
        if isNameTaken:
            return Response("Name already taken", status=status.HTTP_400_BAD_REQUEST)
        isNameTooShort = len(name) < 3
        if isNameTooShort:
            return Response("Name too short", status=status.HTTP_400_BAD_REQUEST)
        isNameTooLong = len(name) > 30
        if isNameTooLong:
            return Response("Name too long", status=status.HTTP_400_BAD_REQUEST)
        user.name = name
        user.save()
        return Response(self.serializer_class(user).data)

class UserUserName(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        password = request.data['password']
        if not user.check_password(password):
            return Response("Your current password is incorrect", status=status.HTTP_400_BAD_REQUEST)
        user.username = request.data['username']
        isUsernameTaken = User.objects.filter(username=user.username).exists()
        if isUsernameTaken:
            return Response("Username already taken", status=status.HTTP_400_BAD_REQUEST)
        isUsernameTooShort = len(user.username) < 3
        if isUsernameTooShort:
            return Response("Username too short", status=status.HTTP_400_BAD_REQUEST)
        isUsernameTooLong = len(user.username) > 30
        if isUsernameTooLong:
            return Response("Username too long", status=status.HTTP_400_BAD_REQUEST)
        user.save()
        return Response(self.serializer_class(user).data)

class UserPassword(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        password = request.data['password']
        if not user.check_password(password):
            return Response("Your current password is incorrect", status=status.HTTP_400_BAD_REQUEST)
        isPasswordTooShort = len(request.data['newPassword']) < 3
        if isPasswordTooShort:
            return Response("Password too short", status=status.HTTP_400_BAD_REQUEST)
        isPasswordTooLong = len(request.data['newPassword']) > 30
        if isPasswordTooLong:
            return Response("Password too long", status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data['newPassword'])
        user.save()
        return Response("Password changed", status=status.HTTP_200_OK)

class UserTeams(generics.ListAPIView):
    serializer_class = TeamReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        players = Player.objects.filter(user=user)
        if players.exists():
            teams = Team.objects.filter(players__in=players)
            if teams.exists():
                return teams
        return Team.objects.none()

class UserTournaments(generics.ListAPIView):
    serializer_class = TournamentReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Tournament.objects.filter(user=user)

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

class DisciplineList(generics.ListAPIView):
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

class TournamentModify(generics.CreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.organizer:
            return Response("User is not an organizer", status=status.HTTP_403_FORBIDDEN)
        isOrganizerFull = Tournament.objects.filter(user=user).count() >= 5
        if isOrganizerFull:
            return Response("Organizer has reached the maximum number of tournaments", status=status.HTTP_400_BAD_REQUEST)
        name = request.data['name']
        isNameTaken = Tournament.objects.filter(name=name).exists()
        if isNameTaken:
            return Response("Name already taken", status=status.HTTP_400_BAD_REQUEST)
        isNameTooShort = len(name) < 3
        if isNameTooShort:
            return Response("Name too short", status=status.HTTP_400_BAD_REQUEST)
        isNameTooLong = len(name) > 30
        if isNameTooLong:
            return Response("Name too long", status=status.HTTP_400_BAD_REQUEST)
        isTeamCountNegative = request.data['team_count'] < 0
        if isTeamCountNegative:
            return Response("Team count cannot be negative", status=status.HTTP_400_BAD_REQUEST)
        isTeamCountTooHigh = request.data['team_count'] > 64
        if isTeamCountTooHigh:
            return Response("Team count too high", status=status.HTTP_400_BAD_REQUEST)
        isPlayerCountNegative = request.data['player_count'] < 0
        if isPlayerCountNegative:
            return Response("Player count cannot be negative", status=status.HTTP_400_BAD_REQUEST)
        isPlayerCountTooHigh = request.data['player_count'] > 64
        if isPlayerCountTooHigh:
            return Response("Player count too high", status=status.HTTP_400_BAD_REQUEST)
        isSubStartAfterSubStop = request.data['sub_start'] > request.data['sub_stop']
        if isSubStartAfterSubStop:
            return Response("Subscription start must be before subscription stop", status=status.HTTP_400_BAD_REQUEST)
        isGamesStartAfterGamesStop = request.data['games_start'] > request.data['games_stop']
        if isGamesStartAfterGamesStop:
            return Response("Games start must be before games stop", status=status.HTTP_400_BAD_REQUEST)
        isMeetingPlatformInvalidUrl = not request.data['meeting_platform'].startswith('https://')
        if isMeetingPlatformInvalidUrl:
            return Response("Invalid meeting platform URL", status=status.HTTP_400_BAD_REQUEST)
        isStreamingPlatformInvalidUrl = not request.data['streaming_platform'].startswith('https://')
        if isStreamingPlatformInvalidUrl:
            return Response("Invalid streaming platform URL", status=status.HTTP_400_BAD_REQUEST)
        isMeetingPlatformTooLong = len(request.data['meeting_platform']) > 200
        if isMeetingPlatformTooLong:
            return Response("Meeting platform URL too long", status=status.HTTP_400_BAD_REQUEST)
        isStreamingPlatformTooLong = len(request.data['streaming_platform']) > 200
        if isStreamingPlatformTooLong:
            return Response("Streaming platform URL too long", status=status.HTTP_400_BAD_REQUEST)
        request.data['user'] = user.id
        return self.create(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        tournament = self.get_object()
        user = request.user
        isOrganizer = tournament.user == user
        if not isOrganizer:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        tournament.delete()

class TournamentDetail(generics.RetrieveAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentReadSerializer

class TournamentName(generics.UpdateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        user = request.user
        tournament = self.get_object()
        if tournament.user != user:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        name = request.data['name']
        isNameTaken = Tournament.objects.filter(name=name).exists()
        if isNameTaken:
            return Response("Name already taken", status=status.HTTP_400_BAD_REQUEST)
        isNameTooShort = len(name) < 3
        if isNameTooShort:
            return Response("Name too short", status=status.HTTP_400_BAD_REQUEST)
        isNameTooLong = len(name) > 30
        if isNameTooLong:
            return Response("Name too long", status=status.HTTP_400_BAD_REQUEST)
        tournament.name = name
        tournament.save()
        return Response(self.serializer_class(tournament).data)
    
class TournamentDiscipline(generics.UpdateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        user = request.user
        tournament = self.get_object()
        if tournament.user != user:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        tournament.discipline = Discipline.objects.get(id=request.data['discipline'])
        tournament.save()
        return Response(self.serializer_class(tournament).data)
    
class TournamentStreamingPlatform(generics.UpdateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        user = request.user
        tournament = self.get_object()
        if tournament.user != user:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        streaming_platform = request.data['streaming_platform']
        isInvalidUrl = not streaming_platform.startswith('https://')
        if isInvalidUrl:
            return Response("Invalid streaming platform URL", status=status.HTTP_400_BAD_REQUEST)
        isTooLong = len(streaming_platform) > 200
        if isTooLong:
            return Response("Streaming platform URL too long", status=status.HTTP_400_BAD_REQUEST)
        tournament.streaming_platform = streaming_platform
        tournament.save()
        return Response(self.serializer_class(tournament).data)
    
class TournamentMeetingPlatform(generics.UpdateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        user = request.user
        tournament = self.get_object()
        if tournament.user != user:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        meeting_platform = request.data['meeting_platform']
        isInvalidUrl = not meeting_platform.startswith('https://')
        if isInvalidUrl:
            return Response("Invalid meeting platform URL", status=status.HTTP_400_BAD_REQUEST)
        isTooLong = len(meeting_platform) > 200
        if isTooLong:
            return Response("Meeting platform URL too long", status=status.HTTP_400_BAD_REQUEST)
        tournament.meeting_platform = meeting_platform
        tournament.save()
        return Response(self.serializer_class(tournament).data)

class TournamentDates(generics.UpdateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        user = request.user
        tournament = self.get_object()
        if tournament.user != user:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        isSubStartAfterSubStop = request.data['sub_start'] > request.data['sub_stop']
        if isSubStartAfterSubStop:
            return Response("Subscription start must be before subscription stop", status=status.HTTP_400_BAD_REQUEST)
        isGamesStartAfterGamesStop = request.data['games_start'] > request.data['games_stop']
        if isGamesStartAfterGamesStop:
            return Response("Games start must be before games stop", status=status.HTTP_400_BAD_REQUEST)
        tournament.sub_start = request.data['sub_start']
        tournament.sub_stop = request.data['sub_stop']
        tournament.games_start = request.data['games_start']
        tournament.games_stop = request.data['games_stop']
        tournament.save()
        return Response(self.serializer_class(tournament).data)

class TournamentCanSubscribe(generics.RetrieveAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        tournament = self.get_object()
        isTooEarly = timezone.now() < tournament.sub_start
        if isTooEarly:
            return Response("Too early to subscribe", status=status.HTTP_400_BAD_REQUEST)
        isTooLate = timezone.now() > tournament.sub_stop
        if isTooLate:
            return Response("Too late to subscribe", status=status.HTTP_400_BAD_REQUEST)
        isAlreadyInTournament = Player.objects.filter(user=user, team__tournament=tournament).exists()
        if isAlreadyInTournament:
            return Response("Already subscribed", status=status.HTTP_400_BAD_REQUEST)
        isTournamentOrganizer = tournament.user == user
        if isTournamentOrganizer:
            return Response("Organizer cannot subscribe", status=status.HTTP_400_BAD_REQUEST)
        return Response(True)

class TeamModify(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        tournament = Tournament.objects.get(id=request.data['tournament'])
        isOrganizer = tournament.user == user
        if isOrganizer:
            return Response("Organizer cannot subscribe", status=status.HTTP_400_BAD_REQUEST)
        isOwnerFull = Team.objects.filter(user=user).count() >= 5
        if isOwnerFull:
            return Response("User has reached the maximum number of teams as owner", status=status.HTTP_400_BAD_REQUEST)
        isTournamentFull = tournament.teams.count() >= tournament.team_count
        if isTournamentFull:
            return Response("Tournament is full", status=status.HTTP_400_BAD_REQUEST)
        isTooEarly = timezone.now() < tournament.sub_start
        if isTooEarly:
            return Response("Too early to subscribe", status=status.HTTP_400_BAD_REQUEST)
        isTooLate = timezone.now() > tournament.sub_stop
        if isTooLate:
            return Response("Too late to subscribe", status=status.HTTP_400_BAD_REQUEST)
        isSubscribed = Player.objects.filter(user=user, team__tournament=tournament).exists()
        if isSubscribed:
            return Response("Already subscribed", status=status.HTTP_400_BAD_REQUEST)
        nameTaken = Team.objects.filter(name=request.data['name'], tournament=tournament).exists()
        if nameTaken:
            return Response("Name already taken", status=status.HTTP_400_BAD_REQUEST)
        tagTaken = Team.objects.filter(tag=request.data['tag'], tournament=tournament).exists()
        if tagTaken:
            return Response("Tag already taken", status=status.HTTP_400_BAD_REQUEST)
        request.data['user'] = request.user.id
        Request.objects.filter(sender=user, team__tournament=tournament).delete()
        return self.create(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        team = self.get_object()
        user = self.request.user
        if team.user != user:
            return Response("User is not the team owner", status=status.HTTP_403_FORBIDDEN)
        nameTaken = Team.objects.filter(name=request.data['name'], tournament=team.tournament).exists()
        if nameTaken:
            return Response("Name already taken", status=status.HTTP_400_BAD_REQUEST)
        tagTaken = Team.objects.filter(tag=request.data['tag'], tournament=team.tournament).exists()
        if tagTaken:
            return Response("Tag already taken", status=status.HTTP_400_BAD_REQUEST)
        team.name = request.data['name']
        team.tag = request.data['tag']
        team.save()
        return Response(self.serializer_class(team).data)
    def delete(self, request, *args, **kwargs):
        team = self.get_object()
        user = self.request.user
        if team.user != user:
            return Response("User is not the team owner", status=status.HTTP_403_FORBIDDEN)
        team.delete()
        return Response("Team deleted", status=status.HTTP_200_OK)

class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamReadSerializer
    
class TeamTransferOwnership(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        team = self.get_object()
        user = self.request.user
        if team.user != user:
            return Response("User is not the team owner", status=status.HTTP_403_FORBIDDEN)
        newOwner = User.objects.get(id=request.data['newOwner'])
        isNewOwnerFull = Team.objects.filter(user=newOwner).count() >= 5
        if isNewOwnerFull:
            return Response("User has reached the maximum number of teams as owner", status=status.HTTP_400_BAD_REQUEST)
        if not Player.objects.filter(user=newOwner, team=team).exists():
            return Response("User is not in the team", status=status.HTTP_400_BAD_REQUEST)
        if newOwner == user:
            return Response("User is already the team owner", status=status.HTTP_400_BAD_REQUEST)
        team.user = newOwner
        team.save()
        Request.objects.filter(sender=newOwner, team__tournament=team.tournament).delete()
        requests = Request.objects.filter(receiver=user, team=team)
        for request in requests:
            request.receiver = newOwner
            request.save()
        return Response(self.serializer_class(team).data)
    
class TeamLogo(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        team = self.get_object()
        user = self.request.user
        if team.user != user:
            return Response("User is not the team owner", status=status.HTTP_403_FORBIDDEN)
        logo = request.FILES.get('logo')
        exists = logo is not None
        if not exists:
            return Response("No logo provided", status=status.HTTP_400_BAD_REQUEST)
        isPng = logo.content_type == 'image/png'
        if not isPng:
            return Response("Logo must be a PNG image", status=status.HTTP_400_BAD_REQUEST)
        isValidSize = logo.size <= 2048 * 2048 * 2
        if not isValidSize:
            return Response("Logo must be smaller than 8MB", status=status.HTTP_400_BAD_REQUEST)
        try:
            image = Image.open(logo)
            width, height = image.size
            isTooBig = width > 2048 or height > 2048
            if isTooBig:
                return Response("Logo must be smaller than 2048x2048", status=status.HTTP_400_BAD_REQUEST)
            isTooSmall = width < 128 or height < 128
            if isTooSmall:
                return Response("Logo must be bigger than 128x128", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Invalid image", status=status.HTTP_400_BAD_REQUEST)
        team.logo = logo
        team.save()
        return Response(self.serializer_class(team).data)
    def delete(self, request, *args, **kwargs):
        team = self.get_object()
        user = self.request.user
        if team.user != user:
            return Response("User is not the team owner", status=status.HTTP_403_FORBIDDEN)
        team.logo = None
        team.save()
        return Response(self.serializer_class(team).data)

class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameReadSerializer

class GameModify(generics.CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(request.data)
        user = request.user
        team1 = Team.objects.get(id=request.data['team1'])
        team2 = Team.objects.get(id=request.data['team2'])
        tournament = Tournament.objects.get(id=request.data['tournament'])
        isOrganizer = tournament.user == user
        if not isOrganizer:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        teamsNotInTournament = team1.tournament != tournament or team2.tournament != tournament
        if teamsNotInTournament:
            return Response("At least one of the teams is not in the tournament", status=status.HTTP_400_BAD_REQUEST)
        teamIsSame = team1 == team2
        if teamIsSame:
            return Response("Team cannot play against itself", status=status.HTTP_400_BAD_REQUEST)
        isDurationNegative = request.data['minutes'] < 0
        if isDurationNegative:
            return Response("Duration cannot be negative", status=status.HTTP_400_BAD_REQUEST)
        areScoresNegative = request.data['score1'] < 0 or request.data['score2'] < 0
        if areScoresNegative:
            return Response("Scores cannot be negative", status=status.HTTP_400_BAD_REQUEST)
        time = datetime.fromisoformat(request.data['timestamp']).timestamp()
        isTooEarly = time < tournament.games_start.timestamp()
        if isTooEarly:
            return Response("Game cannot be played before the tournament starts", status=status.HTTP_400_BAD_REQUEST)
        isTooLate = time > tournament.games_stop.timestamp()
        if isTooLate:
            return Response("Game cannot be played after the tournament ends", status=status.HTTP_400_BAD_REQUEST)
        return self.create(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        game = self.get_object()
        user = request.user
        tournament = game.tournament
        isOrganizer = tournament.user == user
        if not isOrganizer:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        game.delete()
        return Response("Game deleted", status=status.HTTP_200_OK)

class GameTeams(generics.UpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        game = self.get_object()
        user = self.request.user
        tournament = game.tournament
        isOrganizer = tournament.user == user
        if not isOrganizer:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        team1 = Team.objects.get(id=request.data['team1'])
        team2 = Team.objects.get(id=request.data['team2'])
        teamsNotInTournament = team1.tournament != tournament or team2.tournament != tournament
        if teamsNotInTournament:
            return Response("At least one of the teams is not in the tournament", status=status.HTTP_400_BAD_REQUEST)
        teamIsSame = team1 == team2
        if teamIsSame:
            return Response("Team cannot play against itself", status=status.HTTP_400_BAD_REQUEST)
        game.team1 = team1
        game.team2 = team2
        game.save()
        return Response(self.serializer_class(game).data)
    
class GameScore(generics.UpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        game = self.get_object()
        user = self.request.user
        tournament = game.tournament
        isOrganizer = tournament.user == user
        if not isOrganizer:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        areScoresNegative = request.data['score1'] < 0 or request.data['score2'] < 0
        if areScoresNegative:
            return Response("Scores cannot be negative", status=status.HTTP_400_BAD_REQUEST)
        game.score1 = request.data['score1']
        game.score2 = request.data['score2']
        game.save()
        return Response(self.serializer_class(game).data)
    
class GameTime(generics.UpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        game = self.get_object()
        user = self.request.user
        tournament = game.tournament
        isOrganizer = tournament.user == user
        if not isOrganizer:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        time = datetime.fromisoformat(request.data['timestamp']).timestamp()
        isTooEarly = time < tournament.games_start.timestamp()
        if isTooEarly:
            return Response("Game cannot be played before the tournament starts", status=status.HTTP_400_BAD_REQUEST)
        isTooLate = time > tournament.games_stop.timestamp()
        if isTooLate:
            return Response("Game cannot be played after the tournament ends", status=status.HTTP_400_BAD_REQUEST)
        game.timestamp = request.data['timestamp']
        game.save()
        return Response(self.serializer_class(game).data)
    
class GameMinutes(generics.UpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        game = self.get_object()
        user = self.request.user
        tournament = game.tournament
        isOrganizer = tournament.user == user
        if not isOrganizer:
            return Response("User is not the organizer of the tournament", status=status.HTTP_403_FORBIDDEN)
        isDurationNegative = request.data['minutes'] < 0
        if isDurationNegative:
            return Response("Duration cannot be negative", status=status.HTTP_400_BAD_REQUEST)
        game.minutes = request.data['minutes']
        game.save()
        return Response(self.serializer_class(game).data)

class GameDetail(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameReadSerializer

class PlayerDetail(generics.DestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        player = self.get_object()
        user = self.request.user
        isTeamOwner = player.team.user == user
        isLeavingTeam = player.user == user
        if isTeamOwner and isLeavingTeam:
            return Response("Team owners cannot leave the team. Either transfer the ownership first or delete the team", status=status.HTTP_403_FORBIDDEN)
        if isTeamOwner or isLeavingTeam:
            player.delete()
            return Response("Player deleted", status=status.HTTP_200_OK)
        return Response("User is not the player, nor the team owner", status=status.HTTP_403_FORBIDDEN)

class RequestCreate(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = self.request.user
        isTeamOwner = Team.objects.filter(user=user).exists()
        if isTeamOwner:
            return Response("Team owners cannot send requests", status=status.HTTP_403_FORBIDDEN)
        isPlayerFull = Player.objects.filter(user=user).count() >= 5
        if isPlayerFull:
            return Response("User has reached the maximum number of teams as player", status=status.HTTP_400_BAD_REQUEST)
        team = Team.objects.get(id=request.data['team'])
        tournament = team.tournament
        isOrganizer = tournament.user == user
        if isOrganizer:
            return Response("Organizer cannot send requests", status=status.HTTP_403_FORBIDDEN)
        receiver = User.objects.get(id=request.data['receiver'])
        receiverIsNotTeamOwner = team.user != receiver
        if receiverIsNotTeamOwner:
            return Response("Receiver is not the team owner", status=status.HTTP_400_BAD_REQUEST)
        isTooEarly = timezone.now() < tournament.sub_start
        if isTooEarly:
            return Response("Too early to send requests", status=status.HTTP_400_BAD_REQUEST)
        isTooLate = timezone.now() > tournament.sub_stop
        if isTooLate:
            return Response("Too late to send requests", status=status.HTTP_400_BAD_REQUEST)
        isAlreadyInTeam = Player.objects.filter(user=receiver, team=team).exists()
        if isAlreadyInTeam:
            return Response("Receiver is already in the team", status=status.HTTP_400_BAD_REQUEST)
        isAlreadyRequested = Request.objects.filter(sender=user, receiver=receiver, team=team).exists()
        if isAlreadyRequested:
            return Response("Request already sent", status=status.HTTP_400_BAD_REQUEST)
        isTeamFull = team.players.count() >= tournament.player_count
        if isTeamFull:
            return Response("Team is full", status=status.HTTP_400_BAD_REQUEST)
        return self.create(request, *args, **kwargs)

class RequestAccept(generics.UpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        user = self.request.user
        request = self.get_object()
        isPlayerFull = Player.objects.filter(user=user).count() >= 5
        if isPlayerFull:
            return Response("User has reached the maximum number of teams as player", status=status.HTTP_400_BAD_REQUEST)
        isReceiver = request.receiver == user
        if not isReceiver:
            return Response("User is not the receiver", status=status.HTTP_403_FORBIDDEN)
        team = request.team
        isTeamOwner = team.user == user
        if not isTeamOwner:
            return Response("User is not the team owner", status=status.HTTP_403_FORBIDDEN)
        isTooEarly = timezone.now() < team.tournament.sub_start
        if isTooEarly:
            return Response("Too early to accept requests", status=status.HTTP_400_BAD_REQUEST)
        isTooLate = timezone.now() > team.tournament.sub_stop
        if isTooLate:
            return Response("Too late to accept requests", status=status.HTTP_400_BAD_REQUEST)
        isTeamFull = team.players.count() >= team.tournament.player_count
        if isTeamFull:
            return Response("Team is full", status=status.HTTP_400_BAD_REQUEST)
        isPlayerAlreadyInTeam = Player.objects.filter(user=request.sender, team=team).exists()
        if isPlayerAlreadyInTeam:
            return Response("Player is already in the team", status=status.HTTP_400_BAD_REQUEST)
        isPlayerAlreadySubscribed = Player.objects.filter(user=request.sender, team__tournament=team.tournament).exists()
        if isPlayerAlreadySubscribed:
            return Response("Player is already subscribed to the tournament", status=status.HTTP_400_BAD_REQUEST)
        player = Player.objects.create(user=request.sender, team=team)
        Request.objects.filter(sender=request.sender).delete()
        return Response(self.serializer_class(request).data)

class RequestDetail(generics.DestroyAPIView):
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