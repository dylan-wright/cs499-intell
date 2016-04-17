'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com

        game/views.py
            Django views
                index
                games
                game_detail
                create
                join
                agents
                agent_detail
                players
                player_detail
                knowledges
                knowledge_detail
                submit_action
                play
                get_status
                get_snippets
'''

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.utils.timezone import datetime, make_aware
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json

# Create your views here.
'''
index
    TODO: redirect to /game/games/ ?
            or
          make better game index

    url         /game/
    template    /game/templates/game/index.html
'''
def index(request):
    return HttpResponse("Game Index")

'''
games
    Currently just a plain html table with started section
    and pending section
    links to join games if logged in
    links to play games if logged in and part of game

    url         /game/games/   
    template    /game/templates/game/games/games.html
'''
def games(request):
    #get current and pending games (started - True/False)
    current = Game.objects.filter(started=True)
    pending = Game.objects.filter(started=False)

    #cotext for authenticated or not
    context = {"current": current,
               "pending": pending,}

    #logged in users get additional info
    #   join/play
    if request.user.is_authenticated():
        context["loggedin"] = True
        context["user"] = request.user
        context["form"] = GameForm()
    else:
        context["loggedin"] = False

    return render(request, "game/games.html", context)

'''
game_detail
    detail of a game id'd by primary key
    GET:
        TODO: make more than to string
    POST:
        starts game (must be owner)
        return to game list

    url         /game/games/pk/
    template    /game/templates/game/games/game_detail.html
'''
@login_required
def game_detail(request, pk):
    #GET - display details of game
    if request.method == "GET":
        context = {"game": Game.objects.get(pk=pk)}
        return render(request, "game/games/game_detail.html", context)
    #POST - if poster is owner then start game early
    elif request.method == "POST":
        game = Game.objects.get(pk=pk)
        if game.creator == request.user:
            game.start()
        #return to games
        return HttpResponseRedirect("../")

'''
create
    create a new game
    user MUST be logged in
    GET:
        returns form for creating new game
    POST:
        send form data to be validated
        TODO: return error message for missing/malformed data
        return to games list

    url         /game/games/create/
    template    /game/templates/game/games/create.html
    form        game.forms.GameForm
'''
@login_required
def create(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            game = Game(scenario=form.cleaned_data["scenario"],
                        creator=request.user,
                        turn_length=form.cleaned_data["turn_length"],
                        next_turn=form.cleaned_data["next_turn"])
            game.save()
            return HttpResponseRedirect("../")
        #TODO: else send error message to user
    else:
        context = {"form": GameForm()}
        return render(request, "game/games/create.html", context)
    #otherwise send new page
    return HttpResponseRedirect("")

'''
join
    if user is logged in then used to attempt to join game
    
    url         /game/games/pk/join/
    template    /game/templates/game/games/join.html
'''
@login_required
def join(request, pk):
    game = Game.objects.get(pk=pk)
    #create player
    player = Player(user=request.user, points=game.scenario.point_num)
    player.save()
    #add to game
    game.add_player(player)

    context = {"startsat": game.next_turn}
    return render(request, "game/games/join.html", context)

'''
models/model_detail
    models: agents, players, knowledges
    used as list and detail pages for game models 
    TODO: remove eventually?
'''
def agents(request):
    context = {"agents": Agent.objects.all()}
    return render(request, "game/agents.html", context)
def agent_detail(request, pk):
    context = {"agent": Agent.objects.get(pk=pk)}
    return render(request, "game/agents/agent_detail.html", context)
def players(request):
    context = {"players": Player.objects.all()}
    return render(request, "game/players.html", context)
def player_detail(request, pk):
    context = {"player": Player.objects.get(pk=pk)}
    return render(request, "game/players/player_detail.html", context)
def knowledges(request):
    context = {"knowledges": Knowledge.objects.all()}
    return render(request, "game/knowledges.html", context)
def knowledge_detail(request, pk):
    context = {"knowledge": Knowledge.objects.get(pk=pk)}
    return render(request, "game/knowledges/knowledge_detail.html", context)

'''
submit_action
    used by js frontend for ajax communication
    POST:
        turn    -   what turn does the client think it is?
    TODO: route to correct player
    TODO: THIS!
    TODO: authenticate user->player
                    player in game.players

    url         /game/play/pk/submit_action/
    template    /game/templates/game/play/submit_action.html
'''
@login_required
def submit_action(request, pk):
    if request.method == "POST":
        #route to player
        game = Game.objects.get(pk=pk)
        if request.user in game.get_users():
            player = game.players.get(user=request.user)
            actionDict = json.loads(str(request.body)[2:-1])

            #does player control?
            agent = Agent.objects.get(pk=actionDict["agent"])
            if agent in player.agent_set.all():
                #what action
                actionName = actionDict["action"]
                action = Action(acttype=actionName)
                if actionName == "misInfo":
                    target_dict = actionDict["target"]
                    action.acttype = actionName
                    action.actdict = json.dumps(target_dict)
                elif actionName not in ["recruit", "research"]:
                    #(what target)
                    targetKey = actionDict["target"]
                    action.acttype = actionName 
                    action.acttarget = targetKey
                action.save()
                agent.action = action
                agent.save()
                print("logging action %s"%(action))

        context = {"response": request.body}
    elif request.method == "GET":
        context = {"response": ""}
    return render(request, "game/play/submit_action.html", context)

'''
play
    used to serve main html page
    templateized for player/user in question
    user must be authenticated and in game
    otherwise send them to game list

    url         /game/play/pk/
    template    /game/templates/game/play/IntellGame.html
'''
def play(request, pk):
    user = request.user
    game = Game.objects.get(pk=pk)
    #verify user is playing game
    if user in game.get_users():
        player = game.players.get(user=user)
        context = {"pointsDisplay": player.points,
                   "turnDisplay": game.turn,
                   "timerDisplay": game.time_till(),
                   "snippets": ["a", "b", "c"],
                   "username": user,
                   "agents": Agent.objects.filter(player=player)}
        return render(request, "game/play/IntellGame.html", context)
    else:
        return HttpResponseRedirect("../../games")

'''
get_status
    used by the front end to get game status data
    to update screen

    url         /game/play/pk/get_status/
'''
@login_required
def get_status(request, pk):
    #get points, turn, time
    game = Game.objects.get(pk=pk)
    if request.user in game.get_users():
        player = game.players.get(user=request.user)
        points = player.points
        turn = game.turn
        messages = Message.objects.filter(player=player)
        data = {"points": points, 
                "turn": turn, 
                "timer": game.time_till(),
                "next_turn_at": int(game.next_turn.timestamp()),
                "messages": serializers.serialize("json", messages)}
        return HttpResponse(json.dumps(data), content_type="application_json")

'''
get_snippets
    used by the front end to get game snippet data
    to update screen

    url         /game/play/pk/get_snippets/
'''
@login_required
def get_snippets(request, pk):
    game = Game.objects.get(pk=pk)
    if request.user in game.get_users():
        events = game.get_snippets()
        data = []
        for event in events.all():
            describedbys = event.describedby_set.all()
            for describedby in describedbys:
                data += [event, describedby.description]
        json = serializers.serialize("json", data)
        return HttpResponse(json, content_type="application_json")

'''
get_characters
    used by the front end to get character data to
    update screen

    url         /game/play/pk/get_characters/
'''
@login_required
def get_characters(request, pk):
    game  = Game.objects.get(pk=pk)
    if request.user in game.get_users():
        events = game.get_snippets()
        data = []
        pks = []
        for event in events.all():
            involveds = event.involved_set.all()
            for involved in involveds:
                if involved.character.pk not in pks:
                    pks += [involved.character.pk]
                    data += [involved.character]
        json = serializers.serialize("json", data)
        return HttpResponse(json, content_type="application_json")

'''
get_locations
    used by the front end to get location data to
    update screen

    url         /game/play/pk/get_locations/
'''
@login_required
def get_locations(request, pk):
    game = Game.objects.get(pk=pk)
    if request.user in game.get_users():
        events = game.get_snippets()
        data = []
        pks = []
        for event in events.all():
            happenedats = event.happenedat_set.all()
            for happenedat in happenedats:
                if happenedat.location.pk not in pks:
                    pks += [happenedat.location.pk]
                    data += [happenedat.location]
        json = serializers.serialize("json", data)
        return HttpResponse(json, content_type="application_json")

'''
get_agents
    used by front end to get agent data to
    update screen

    url         /game/play/pk/get_agents
'''
@login_required
def get_agents(request, pk):
    game = Game.objects.get(pk=pk)
    if request.user in game.get_users():
        data = []
        for player in game.players.all():
            if player.user != request.user:
                data += player.agent_set.all()
        json = serializers.serialize("json", data)
        return HttpResponse(json, content_type="application_json")

'''
get_own_agents
    used by front end to get agent data for
    one player

    url         /game/play/pk/get_own_agents/
'''
@login_required
def get_own_agents(request, pk):
    game = Game.objects.get(pk=pk)
    if request.user in game.get_users():
        data = game.players.get(user=request.user).agent_set.all()
        json = serializers.serialize("json", data)
        return HttpResponse(json, content_type="application_json")
