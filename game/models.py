from django.db import models
from editor.models import Scenario
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import datetime, make_aware

# Create your models here.
'''
Player
    used to represent a particular user in a game

    id -    auto gen primary key
    user -  user being represented
'''
class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

'''
Game
    used to represent a particular game. 

    id -    auto gen primary key
    scenario - scenario being used by the game. Used to determine
                which snippets are presented and win conditions
    started - indicates if the game has started or not. Used to
                determine if players may join and where to put
                the game in the game list view
    creator - User who configured the game. They should have the
                ability to manage it (down the line. at this point
                they will not)
    turn - current turn
    next_turn - datetime of the next turn. When this time is reached
                the game should generate the next round of snippets
                and allow players to access them. Also proccess any
                player actions and determine side effects
    turn-length - dimedelta which determines when the next turn will
                    be. When the turn changes the next_turn field will
                    get this delta added to it
methods
    add_player
    start
    time_till
'''
class Game(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)
    started = models.BooleanField(default=False)
    creator = models.ForeignKey(User, null=True)
    turn = models.IntegerField(default=0)
    next_turn = models.DateTimeField(null=True)
    turn_length = models.DurationField(default=timedelta(days=1))

    def __str__(self):
        return "Game created by %s using scenario %s"%(self.creator.first_name, self.scenario.name)

    '''
    add_player
        I: player - a Player object
        O: player is added to the players field if the game has not started
            otherwise no change
    '''
    def add_player(self, player):
        self.players.add(player)

    '''
    start
        I: 
        O:  started becomes true
    '''
    def start(self):
        self.started = True
        self.next_turn = self.turn_length + datetime.now()
        self.save()

    '''
    time_till
        I:
        O:  if next_turn is defined then return the time till the first turn
            or the time till the next turn
    '''
    def time_till(self):
        now = make_aware(datetime.now())
        if self.next_turn != None:
            till = self.next_turn - now
            return till.seconds

    '''
    start_next_turn
        I:
        O:  increment turn counter, proccess actions, produce snippets,
            set next turn time
    '''
    def start_next_turn(self):
        self.turn += 1
        self.save()
