from .models import Game
from django.utils.timezone import datetime, make_aware

'''
TODO: figure out why cron cannot seem to find this
'''
def check_games():
    current_time = make_aware(datetime.now())
    for game in Game.objects.all():
        game.start_next_turn()
        if current_time > game.next_turn:
            #check if next turn can start
            if game.started:
                game.start_next_turn()
            #check if game is ready to start. If so call start
            else:
                game.start()
