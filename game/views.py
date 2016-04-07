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
