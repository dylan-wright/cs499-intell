from django.db import models
from editor.models import Scenario
from django.contrib.auth.models import User

# Create your models here.
class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Game(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)
    started = models.BooleanField(default=False)
    creator = models.ForeignKey(User, null=True)

    def __str__(self):
        return "Game created by %s using scenario %s"%(creator.name, scenario.name)

    def add_player(self, player):
        self.players.add(player)

    def start(self):
        self.started = True

