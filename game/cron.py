from .models import Game
from django.utils.timezone import datetime, make_aware

def check_games():
    current_time = make_aware(date_time.now())

    for game in Game.objects:
        game.start_next_turn()
        if current_time > game.next_turn:
            #check if next turn can start
            if game.started:
                game.start_next_turn()
            #check if game is ready to start. If so call start
            else:
                game.start()
