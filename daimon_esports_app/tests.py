from django.test import TestCase
from .models import User, Discipline, Tournament, Team, Game, Player, Request
from django.utils import timezone
from django.db.utils import IntegrityError

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username="testuser", password="password123", name="Test User")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("password123"))

    def test_superuser_creation(self):
        superuser = User.objects.create_superuser(username="admin", password="adminpass", name="Admin User")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_unique_id_generation(self):
        user = User.objects.create_user(username="testuser", password="password123")
        self.assertTrue(len(user.id) == 12)
        self.assertTrue(user.id.isalnum())

    def test_str_representation(self):
        user = User.objects.create_user(username="testuser", password="password123", name="Test User")
        self.assertEqual(str(user), "Test User")

class DisciplineModelTest(TestCase):
    def test_discipline_creation(self):
        discipline = Discipline.objects.create(name="Basketball")
        self.assertEqual(discipline.name, "Basketball")

    def test_unique_id_generation(self):
        discipline = Discipline.objects.create(name="Football")
        self.assertTrue(len(discipline.id) == 12)
        self.assertTrue(discipline.id.isalnum())

    def test_str_representation(self):
        discipline = Discipline.objects.create(name="Basketball")
        self.assertEqual(str(discipline), "Basketball")

class TournamentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.discipline = Discipline.objects.create(name="Basketball")

    def test_tournament_creation(self):
        tournament = Tournament.objects.create(
            user=self.user,
            name="Test Tournament",
            sub_start=timezone.now(),
            sub_stop=timezone.now(),
            games_start=timezone.now(),
            games_stop=timezone.now(),
            discipline=self.discipline,
            team_count=8,
            player_count=5,
            meeting_platform="Zoom",
            streaming_platform="Twitch"
        )
        self.assertEqual(tournament.name, "Test Tournament")

    def test_unique_id_generation(self):
        tournament = Tournament.objects.create(
            user=self.user,
            name="Test Tournament",
            sub_start=timezone.now(),
            sub_stop=timezone.now(),
            games_start=timezone.now(),
            games_stop=timezone.now(),
            discipline=self.discipline,
            team_count=8,
            player_count=5,
            meeting_platform="Zoom",
            streaming_platform="Twitch"
        )
        self.assertTrue(len(tournament.id) == 12)
        self.assertTrue(tournament.id.isalnum())

    def test_str_representation(self):
        tournament = Tournament.objects.create(
            user=self.user,
            name="Test Tournament",
            sub_start=timezone.now(),
            sub_stop=timezone.now(),
            games_start=timezone.now(),
            games_stop=timezone.now(),
            discipline=self.discipline,
            team_count=8,
            player_count=5,
            meeting_platform="Zoom",
            streaming_platform="Twitch"
        )
        self.assertEqual(str(tournament), "Test Tournament")

class TeamModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.discipline = Discipline.objects.create(name="Basketball")
        self.tournament = Tournament.objects.create(
            user=self.user,
            name="Test Tournament",
            sub_start=timezone.now(),
            sub_stop=timezone.now(),
            games_start=timezone.now(),
            games_stop=timezone.now(),
            discipline=self.discipline,
            team_count=8,
            player_count=5,
            meeting_platform="Zoom",
            streaming_platform="Twitch"
        )

    def test_team_creation(self):
        team = Team.objects.create(name="Test Team", tag="TT", user=self.user, tournament=self.tournament)
        self.assertEqual(team.name, "Test Team")
        self.assertEqual(team.tag, "TT")

    def test_unique_id_generation(self):
        team = Team.objects.create(name="Test Team", tag="TT", user=self.user, tournament=self.tournament)
        self.assertTrue(len(team.id) == 12)
        self.assertTrue(team.id.isalnum())

    def test_str_representation(self):
        team = Team.objects.create(name="Test Team", tag="TT", user=self.user, tournament=self.tournament)
        self.assertEqual(str(team), "Test Team")

class GameModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.discipline = Discipline.objects.create(name="Basketball")
        self.tournament = Tournament.objects.create(
            user=self.user,
            name="Test Tournament",
            sub_start=timezone.now(),
            sub_stop=timezone.now(),
            games_start=timezone.now(),
            games_stop=timezone.now(),
            discipline=self.discipline,
            team_count=8,
            player_count=5,
            meeting_platform="Zoom",
            streaming_platform="Twitch"
        )
        self.team1 = Team.objects.create(name="Team 1", tag="T1", user=self.user, tournament=self.tournament)
        self.team2 = Team.objects.create(name="Team 2", tag="T2", user=self.user, tournament=self.tournament)

    def test_game_creation(self):
        game = Game.objects.create(
            team1=self.team1,
            team2=self.team2,
            timestamp=timezone.now(),
            minutes=90,
            tournament=self.tournament
        )
        self.assertEqual(game.team1, self.team1)
        self.assertEqual(game.team2, self.team2)

    def test_unique_id_generation(self):
        game = Game.objects.create(
            team1=self.team1,
            team2=self.team2,
            timestamp=timezone.now(),
            minutes=90,
            tournament=self.tournament
        )
        self.assertTrue(len(game.id) == 12)
        self.assertTrue(game.id.isalnum())

    def test_str_representation(self):
        game = Game.objects.create(
            team1=self.team1,
            team2=self.team2,
            timestamp=timezone.now(),
            minutes=90,
            tournament=self.tournament
        )
        self.assertEqual(str(game), "T1 vs T2")

class PlayerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", name="PlayerName")
        self.discipline = Discipline.objects.create(name="Basketball")
        self.tournament = Tournament.objects.create(
            user=self.user,
            name="Test Tournament",
            sub_start=timezone.now(),
            sub_stop=timezone.now(),
            games_start=timezone.now(),
            games_stop=timezone.now(),
            discipline=self.discipline,
            team_count=8,
            player_count=5,
            meeting_platform="Zoom",
            streaming_platform="Twitch"
        )
        self.team = Team.objects.create(name="Team 1", tag="T1", user=self.user, tournament=self.tournament)

    def test_player_creation(self):
        player = Player.objects.create(user=self.user, team=self.team)
        self.assertEqual(player.user, self.user)
        self.assertEqual(player.team, self.team)

    def test_unique_together_constraint(self):
        Player.objects.create(user=self.user, team=self.team)
        with self.assertRaises(IntegrityError):
            Player.objects.create(user=self.user, team=self.team)

    def test_unique_id_generation(self):
        player = Player.objects.create(user=self.user, team=self.team)
        self.assertTrue(len(player.id) == 12)
        self.assertTrue(player.id.isalnum())

    def test_str_representation(self):
        player = Player.objects.create(user=self.user, team=self.team)
        self.assertEqual(str(player), "T1 PlayerName")

class RequestModelTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="password123")
        self.receiver = User.objects.create_user(username="receiver", password="password123")
        discipline = Discipline.objects.create(name="Basketball")
        tournament = Tournament.objects.create(
            user=self.sender,
            name="Test Tournament",
            sub_start=timezone.now(),
            sub_stop=timezone.now(),
            games_start=timezone.now(),
            games_stop=timezone.now(),
            discipline=discipline,
            team_count=8,
            player_count=5,
            meeting_platform="Zoom",
            streaming_platform="Twitch"
        )
        self.team = Team.objects.create(name="Team 1", tag="T1", user=self.sender, tournament=tournament)

    def test_request_creation(self):
        request = Request.objects.create(sender=self.sender, receiver=self.receiver, team=self.team)
        self.assertEqual(request.sender, self.sender)
        self.assertEqual(request.receiver, self.receiver)

    def test_unique_together_constraint(self):
        Request.objects.create(sender=self.sender, receiver=self.receiver, team=self.team)
        with self.assertRaises(IntegrityError):
            Request.objects.create(sender=self.sender, receiver=self.receiver, team=self.team)

    def test_unique_id_generation(self):
        request = Request.objects.create(sender=self.sender, receiver=self.receiver, team=self.team)
        self.assertTrue(len(request.id) == 12)
        self.assertTrue(request.id.isalnum())

    def test_str_representation(self):
        request = Request.objects.create(sender=self.sender, receiver=self.receiver, team=self.team)
        self.assertEqual(str(request), "sender -> receiver")