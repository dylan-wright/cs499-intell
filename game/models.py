from django.db import models
from editor.models import *
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import datetime, make_aware

# Create your models here.
'''
Player
    used to represent a particular user in a game

    id      -   auto gen primary key
    user    -   user being represented
    points  -   number of intell points left
'''
class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return "player controlled by %s"%(user.username)

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
    detail_html - temp used for prototype page
    add_player  - add player to players
    time_till - till next turn. used for nice countdown page
    start - sets started and inits next_turn
    start_next_turn - does turn proccessing
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

    def detail_html(self):
        return "scenario: "+str(self.scenario)
    '''
    add_player
        I: player - a Player object
        O: player is added to the players field if the game has not started
            otherwise no change
    '''
    def add_player(self, player):
        self.players.add(player)
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
        #next turn
        self.turn += 1

        #proccess actions
        for player in self.players.all():
            pass
        #next turn time
        self.next_turn += self.turn_length

        #store in db
        self.save()
    
    '''
    start
        I: 
        O:  started becomes true
            sideffects: players are initialized, start_next_turn used to
            make next turn environment (turn counter, actions, snippets)
            initial agents are created
    '''
    def start(self):
        #init players

        #init game
        self.started = True
        self.next_turn = make_aware(datetime.now())

        #init first turn 
        self.start_next_turn()

        #write to the db
        self.save()



'''
Action
    model tracking an action's target(s)/info

    id      -   auto gen primary key
    acttype -   type of action TODO: fix this
'''
class Action(models.Model):
    acttype = models.CharField(max_length=64) #this is obviously not right
    
    def __str__(self):
        return "Action %s"%(self.acttype)
'''
Agent
    model tracking an Agent's status

    id      -   auto gen primary key
    name    -   Agent name (meaningless but pretty)
    action  -   current action for agent to perform on turn proccessing
    alive   -   is the agent alive
    location-   where the agent is
    player  -   player controlling this agent
'''
class Agent(models.Model):
    name = models.CharField(max_length=64)
    action = models.ForeignKey(Action)
    alive = models.BooleanField(default=True)
    location = models.ManyToManyField(Location, null=True)
    player = models.ForeignKey(Player, null=True) #a null player is an orphaned
                                                  # agent-they cant perform
                                                  # actions

    def __str__(self):
        return "Agent %s"%(str(self.name))

'''
Knowledge
    model relating Players to Events. issued when a player performs an
    investigation on an Event

    event   -   Event model investigated
    turn    -   turn investigation occoured on
'''
class Knowledge(models.Model):
    event = models.ForeignKey(Event, null=True)
    turn = models.IntegerField()

    def __str__(self):
        return "result of investigation of %s on turn %s"%(str(self.event), str(self.turn))

