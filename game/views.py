from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Game Index")

def games(request):
    return render(request, "game/games.html")

def create(request):
    return render(request, "game/games/create.html")
