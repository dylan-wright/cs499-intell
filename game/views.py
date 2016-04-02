from django.shortcuts import render
from django.http import HttpResponse
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
    context = {"form": GameForm()}
    return render(request, "game/games/create.html", context)
