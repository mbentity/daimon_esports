from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
import random

def generate_hex_id(length=12):
    return ''.join(random.choices('0123456789abcdef', k=length))


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
    id = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    organizer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_id()
        super(User, self).save(*args, **kwargs)
    def generate_unique_id(self):
        new_id = generate_hex_id()
        while User.objects.filter(id=new_id).exists():
            new_id = generate_hex_id()
        return new_id
    def __str__(self):
        return self.name

class Discipline(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=255)
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_id()
        super(Discipline, self).save(*args, **kwargs)
    def generate_unique_id(self):
        new_id = generate_hex_id()
        while Discipline.objects.filter(id=new_id).exists():
            new_id = generate_hex_id()
        return new_id
    def __str__(self):
        return self.name

class Tournament(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    sub_start = models.DateTimeField()
    sub_stop = models.DateTimeField()
    games_start = models.DateTimeField()
    games_stop = models.DateTimeField()
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    team_count = models.IntegerField()
    player_count = models.IntegerField()
    meeting_platform = models.CharField(max_length=255)
    streaming_platform = models.CharField(max_length=255)
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_id()
        super(Tournament, self).save(*args, **kwargs)
    def generate_unique_id(self):
        new_id = generate_hex_id()
        while Tournament.objects.filter(id=new_id).exists():
            new_id = generate_hex_id()
        return new_id
    def __str__(self):
        return self.name

class Team(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=4, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_id()
        super(Team, self).save(*args, **kwargs)
    def generate_unique_id(self):
        new_id = generate_hex_id()
        while Team.objects.filter(id=new_id).exists():
            new_id = generate_hex_id()
        return new_id
    def __str__(self):
        return self.name

class Game(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1', null=True)
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2', null=True)
    score1 = models.IntegerField(default=None, blank=True, null=True)
    score2 = models.IntegerField(default=None, blank=True, null=True)
    timestamp = models.DateTimeField()
    minutes = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_id()
        super(Game, self).save(*args, **kwargs)
    def generate_unique_id(self):
        new_id = generate_hex_id()
        while Game.objects.filter(id=new_id).exists():
            new_id = generate_hex_id()
        return new_id
    def __str__(self):
        return self.team1.tag + ' vs ' + self.team2.tag

class Player(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'team')
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_id()
        super(Player, self).save(*args, **kwargs)
    def generate_unique_id(self):
        new_id = generate_hex_id()
        while Player.objects.filter(id=new_id).exists():
            new_id = generate_hex_id()
        return new_id
    def __str__(self):
        return self.team.tag + ' ' + self.user.name

class Request(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    class Meta:
        unique_together = ('sender', 'receiver')
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_id()
        super(Request, self).save(*args, **kwargs)
    def generate_unique_id(self):
        new_id = generate_hex_id()
        while Request.objects.filter(id=new_id).exists():
            new_id = generate_hex_id()
        return new_id
    def __str__(self):
        return self.sender.username + ' -> ' + self.receiver.username