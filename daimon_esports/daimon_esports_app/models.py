from django.db import models

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    display = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)
    organizer = models.BooleanField()

class Discipline(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

class Tournament(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # utility info: dates
    sub_start = models.DateTimeField()
    sub_stop = models.DateTimeField()
    games_start = models.DateTimeField()
    games_stop = models.DateTimeField()
    # tournament details
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    team_count = models.IntegerField()
    player_count = models.IntegerField()
    # platforms
    meeting_platform = models.CharField(max_length=255)
    streaming_platform = models.CharField(max_length=255)

class Roster(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

class Game(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    roster1 = models.CharField(max_length=255)
    roster2 = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    minutes = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

class Player(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'roster')

class Request(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    class Meta:
        unique_together = ('sender', 'receiver')