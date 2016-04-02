from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *

# Create your views here.
def index(request):
    return HttpResponse("Game Index")

def games(request):
    context = {"current": Game.objects.filter(started=True),
               "pending": Game.objects.filter(started=False)
              }
    return render(request, "game/games.html", context)

def create(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            game = Game(scenario=form.cleaned_data["scenario"],
                        creator=form.cleaned_data["creator"])
            game.save()
            return HttpResponseRedirect("../")
    else:
        context = {"form": GameForm()}
    return render(request, "game/games/create.html", context)
