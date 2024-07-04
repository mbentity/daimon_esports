from django.db import models
import random

def generate_hex_id(length=12):
    return ''.join(random.choices('0123456789abcdef', k=length))


# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    display = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)
    organizer = models.BooleanField()
    def save(self, *args, **kwargs):
        self.id = self.generate_unique_id()
        super(User, self).save(*args, **kwargs)
    def generate_unique_id(self):
        new_id = generate_hex_id()
        while User.objects.filter(id=new_id).exists():
            new_id = generate_hex_id()
        return new_id
    def __str__(self):
        return self.username

class Discipline(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=255)
    def save(self, *args, **kwargs):
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
    def save(self, *args, **kwargs):
        self.id = self.generate_unique_id()
        super(Tournament, self).save(*args, **kwargs)
    def generate_unique_id(self):
        new_id = generate_hex_id()
        while Tournament.objects.filter(id=new_id).exists():
            new_id = generate_hex_id()
        return new_id
    def __str__(self):
        return self.name

class Roster(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=4, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        self.id = self.generate_unique_id()
        super(Roster, self).save(*args, **kwargs)
    def generate_unique_id(self):
        new_id = generate_hex_id()
        while Roster.objects.filter(id=new_id).exists():
            new_id = generate_hex_id()
        return new_id
    def __str__(self):
        return self.name

class Game(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    roster1 = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name='roster1')
    roster2 = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name='roster2')
    timestamp = models.DateTimeField()
    minutes = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        self.id = self.generate_unique_id()
        super(Game, self).save(*args, **kwargs)
    def generate_unique_id(self):
        new_id = generate_hex_id()
        while Game.objects.filter(id=new_id).exists():
            new_id = generate_hex_id()
        return new_id
    def __str__(self):
        return self.roster1.tag + ' vs ' + self.roster2.tag

class Player(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'roster')
    def save(self, *args, **kwargs):
        self.id = self.generate_unique_id()
        super(Player, self).save(*args, **kwargs)
    def generate_unique_id(self):
        new_id = generate_hex_id()
        while Player.objects.filter(id=new_id).exists():
            new_id = generate_hex_id()
        return new_id
    def __str__(self):
        return self.roster.tag + ' ' + self.user.display

class Request(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    class Meta:
        unique_together = ('sender', 'receiver')
    def save(self, *args, **kwargs):
        self.id = self.generate_unique_id()
        super(Request, self).save(*args, **kwargs)
    def generate_unique_id(self):
        new_id = generate_hex_id()
        while Request.objects.filter(id=new_id).exists():
            new_id = generate_hex_id()
        return new_id
    def __str__(self):
        return self.sender.username + ' -> ' + self.receiver.username