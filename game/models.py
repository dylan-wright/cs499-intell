'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com

        game/models.py
            Django models for game app
                Player
                Game
                Agent
                Action
                Knowledge
'''

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
        return "player controlled by %s"%(self.user.username)

    def add_agent(self):
        action = Action()
        action.save()
        agent = Agent(name="", alive=True, action=action, player=self)
        agent.save()

    '''
    get_knowledge
        returns the QuerySet of all Knowledge objects associated with
        the player
    '''
    def get_knowledge(self):
        return Knowledge.objects.filter(player=self).all()

    '''
    get_messages
        returns QuerySet of all Message objects associated with
        the player
    '''
    def get_messages(self):
        return Message.objects.filter(player=self).all()

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
    
    #TODO: make these configured in game create?
    #       would require more fields default values are same
    ACTION_COSTS = {"tail": 1, "investigate": 1, "misinf": 1, "check": 1,
                    "recruit": 3, "apprehend": 5, "terminate": 5, 
                    "research": -2}


    def __str__(self):
        return "Game using scenario %s"%(self.scenario.name)

    def detail_html(self):
        return "scenario: "+str(self.scenario)

    def get_users(self):
        users = []
        for player in self.players.all():
            users += [player.user]
        return users
    '''
    add_player
        I: player - a Player object
        O: player is added to the players field if the game has not started
            and the player is not in the game already
            otherwise no change
    '''
    def add_player(self, player):
        if player not in self.players.all():
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
            #otherwise get large ugly number of seconds
            if now > self.next_turn:
                return 0
            else:
                till = self.next_turn - now
                return till.seconds
        
    
    '''
    is_target_valid
        I:  an action
        O:  bool representing if the action is valid (acttarget exists in
            the appropriate table in the appropriate game
            If an invalid action is sent generate a Message object for
            the player
    '''
    def is_target_valid(self, action):
        acttype = action.acttype
        acttarget = action.acttarget
        player = action.agent_set.all()[0].player
        message = Message(player=player, turn=self.turn)

        #determine target table
        #this is evil TODO: change it to if/elif/else
        try:
            target_table = {"tail": Character,
                            "investigate": Location,
                            "check": Description,
                            "misinf": None,
                            "recruit": None,
                            "apprehend": Character,
                            "research": None,
                            "terminate": Agent}[acttype]
        except (KeyError):
            message.text = "bad action type"
            message.save()
            return False

        if target_table != None:
            targets = target_table.objects.filter(pk=acttarget)
            #should only match one target
            if len(targets) == 1:
                target = targets[0]
                #is the target in the scenario for this game
                events = self.scenario.event_set.all()
                if target_table == Character:
                    #find events involving the character in this game
                    event_qset = events.filter(involved=Involved.objects.filter(character=target))
                elif target_table == Location:
                    #find events happenedat the location in this game
                    event_qset = events.filter(happenedat=HappenedAt.objects.filter(location=target))
                elif target_table == Description:
                    #find events describedby the description in this game
                    event_qset = events.filter(describedby=DescribedBy.objects.filter(description=target))
                elif target_table == Agent:
                    #find agents in this game
                    agent_qset = Agent.objects.filter(player__in=self.players.all())
                    if target in agent_qset.all():
                        return True
                    else:
                        message.text = "Agent not found"
                        message.save()
                        return False
                else:
                    message.text = "target table not found"
                    messave.save()
                    return False

                if len(event_qset) == 1:
                    if event_qset[0] in event_qset.all():
                        return True
                    else:
                        message.text = "Event not found"
                        message.save()
                        return False
                else:
                    message.text = "ambiguous set of events"
                    message.save()
                    return False
            else:
                message.text = "ambiguous target pk"
                message.save()
                return False
        else:
            #any invalid acttype will throw a key error
            #so dont worry about bad acttype 
            return True
            
    '''
    start_next_turn
        I:
        O:  increment turn counter, proccess actions, produce snippets,
            set next turn time
    '''
    def start_next_turn(self):
        #next turn
        self.turn += 1
        
        #process actions
        agents_to_proc = []
        for player in self.players.all():
            #add agents to list
            agents_to_proc += Agent.objects.filter(player=player)

        #TODO: decide on order of agents?
        for agent in agents_to_proc:
            acttype = agent.action.acttype
            if acttype in self.ACTION_COSTS.keys():
                #can player afford it?
                #TODO: player with multiple agents - can they afford
                #       all actions? if not how to decide?
                #       first (agent) come first served?
                if agent.player.points >= self.ACTION_COSTS[acttype]:
                    #is the target valid?
                    if self.is_target_valid(agent.action):
                        self.perform_action(agent.action)
                    else:
                        #action target invalid
                        #message generated by is_target_valid
                        pass
                else:
                    #player has too few points
                    message = Message(player=agent.player, turn=self.turn,
                                      text="too few points to perform %s"%(agent.action))
                    message.save()
            else:
                #action does not exist
                message = Message(player=agent.player, turn=self.turn,
                                  text="action %s does not exist"%(agent.action))
                message.text = "action doesnt exist"
                message.save()

        #next turn time
        self.next_turn += self.turn_length

        #store in db
        self.save()

    
    '''
    perform_action
        I:  an action that has been verified
        O:  action performed, knowledge created,
            side effects effected

        If the action is valid (assumed) then the action will 
        succeed (oh hello hubris)

        TODO: tail, investigate, check, misinf, apprehend, terminate
    '''
    def perform_action(self, action):
        player = action.agent_set.all()[0].player

        if action.acttype == "tail":
            involveds = Involved.objects.filter(character__id=action.acttarget)
            for involved in involveds.all():
                if involved.event.turn < self.turn:
                    knowledge = Knowledge(player=player, turn=self.turn,
                                          event=involved.event)
                    knowledge.save()
                    describedbys = DescribedBy.objects.filter(event=involved.event)
                    for describedby in describedbys.all():
                        if describedby.description.hidden:
                            message = Message()
                            message.player = player
                            message.turn=self.turn
                            #TODO fix this
                            message.text = "Tailing %s discovered that %s"%(Character.objects.get(pk=action.acttarget),
                                                                            describedby.description)
                            message.save()
        elif action.acttype == "investigate":
            happenedats = HappenedAt.objects.filter(location__id=action.acttarget)
            for happenedat in happenedats:
                if happenedat.event.turn < self.turn:
                    knowledge = Knowledge(player=player, turn=self.turn,
                                          event=happenedat.event)
                    knowledge.save()
                    describedbys = DescribedBy.objects.filter(event=happenedat.event)
                    for describedby in describedbys.all():
                        if describedby.description.hidden:
                            message = Message()
                            message.player = player
                            message.turn = self.turn
                            #TODO fix this
                            message.text = "Ivestigation into %s discovered that %s"%(Location.objects.get(pk=action.acttarget), 
                                                                                      describedby.description)
                            message.save()
        elif action.acttype == "check":
            describedby = DescribedBy.objects.get(description__id=action.acttarget)
            if describedby.event.turn < self.turn:
                knowledge = Knowledge(player=player, turn=self.turn,
                                      event=describedby.event)
                knowledge.save()
                if describedby.event.misinf:
                    message = Message()
                    message.player = player
                    message.turn = self.turn
                    #TODO: fix this
                    message.text = "The informationt that '%s' has been proven to be false"%(Description.objects.get(pk=action.acttarget))
                    message.save()
        elif action.acttype == "misinf":
            pass
        elif action.acttype == "recruit":
            #player gets another agent
            #TODO: test to ensure new agents cant act
            #       also that dummy action created has no side effects
            #       (should just be recorded as an invalid action by
            #        game.Game.start_next_turn)
            player.add_agent()
        elif action.acttype == "apprehend":
            pass
        elif action.acttype == "research":
            #only need to sub (negative) action cost from player
            pass
        elif action.acttype == "terminate":
            pass
        player.points -= self.ACTION_COSTS[action.acttype]
        player.save()

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
        for player in self.players.all():
            #all players get an agent
            player.add_agent()

        #init game
        self.started = True
        self.next_turn = make_aware(datetime.now())
        self.save()

        #init first turn 
        self.start_next_turn()

    def get_snippets(self):
        events = Event.objects.filter(scenario=self.scenario,
                                      turn__lt=self.turn)
        
        return events
        

'''
Action
    model tracking an action's target(s)/info

    id          -   auto gen primary key
    acttype     -   type of action TODO: fix this
    acttarget   -   target of action
                    is the pk of the intended target game processing step
                    should determine if target is legal
'''
class Action(models.Model):
    acttype = models.CharField(max_length=64) #this is obviously not right
    acttarget = models.IntegerField(default=-1)


    
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
    location = models.ManyToManyField(Location)
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
    player = models.ForeignKey(Player, null=True)

    def __str__(self):
        return "result of investigation of %s on turn %s"%(str(self.event), str(self.turn))

'''
Message
    model representing game status messages to be relayed to the player
    on a particular turn. Generated when turn is processed due to:
        errors in action sent
        sucessfull actions
        unsucessfull actions
        agent termination
        ... TODO:add more

    id      -   autogen primary key
    player  -   player owning message
    text    -   text of the message
    turn    -   turn messege was generated on
    ... TODO: add more
'''
class Message(models.Model):
    player = models.ForeignKey(Player)
    text = models.CharField(max_length=512) # is .5KB enough? (hopefully)
    turn = models.IntegerField()

    def __str__(self):
        return self.text
