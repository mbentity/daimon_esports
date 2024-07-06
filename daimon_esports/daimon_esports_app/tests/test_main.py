from django.test import TestCase
from models import User, Discipline, Tournament, Roster, Game, Player, Request

class TestUser(TestCase):
    def test_user(self):
        user = User.objects.create(username='testuser', password='testpassword')

class TestDiscipline(TestCase):
    def test_discipline(self):
        discipline = Discipline.objects.create(name='testdiscipline')

class TestTournament(TestCase):
    def test_tournament(self):
        tournament = Tournament.objects.create(name='testtournament')

class TestRoster(TestCase):
    def test_roster(self):
        roster = Roster.objects.create(name='testroster')

class TestGame(TestCase):
    def test_game(self):
        game = Game.objects.create(name='testgame')

class TestPlayer(TestCase):
    def test_player(self):
        player = Player.objects.create(name='testplayer')

class TestRequest(TestCase):
    def test_request(self):
        request = Request.objects.create(name='testrequest')