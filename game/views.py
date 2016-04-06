from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.utils.timezone import datetime, make_aware

# Create your views here.
def index(request):
    return HttpResponse("Game Index")

def games(request):
    current = Game.objects.filter(started=True)
    pending = Game.objects.filter(started=False)

    context = {"current": current,
               "pending": pending,
              }
    return render(request, "game/games.html", context)

def game_detail(request, pk):
    if request.method == "GET":
        context = {"game": Game.objects.get(pk=pk)}
        return render(request, "game/games/game_detail.html", context)
    elif request.method == "POST":
        Game.objects.get(pk=pk).start()
        return HttpResponseRedirect("../")

def create(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            game = Game(scenario=form.cleaned_data["scenario"],
                        creator=form.cleaned_data["creator"],
                        turn_length=form.cleaned_data["turn_length"])
            game.save()
            return HttpResponseRedirect("../")
    else:
        context = {"form": GameForm()}
    return render(request, "game/games/create.html", context)

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
