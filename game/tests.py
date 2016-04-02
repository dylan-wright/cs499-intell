from django.test import TestCase
from .models import *
from editor.models import Scenario
from django.contrib.auth.models import User

# Create your tests here.
class  GameTestCase(TestCase):
    def setUp(self):
        Scenario.objects.create(name="test",
                                turn_num=20,
                                point_num=20,
                                author="test",
                                file_name="fixture.json")
        Game.objects.create(scenario=Scenario.objects.all()[0])

    def test_games_init(self):
        '''game initialized and players can be added'''
        game = Game.objects.get(pk=1)
        scenario = game.scenario
        
        self.assertEqual(scenario.name, "test")
        self.assertEqual(scenario.turn_num, 20)
        self.assertEqual(scenario.point_num, 20)
        self.assertEqual(scenario.author, "test")
        self.assertEqual(scenario.file_name, "fixture.json")

        self.assertEqual(game.started, False)

        u1 = User(username="user1", first_name="Test 1")
        u2 = User(username="user2", first_name="Test 2")
        u3 = User(username="user3", first_name="Test 3")
        
        u1.save()
        u2.save()
        u3.save()

        p1 = Player(user=u1)
        p2 = Player(user=u2)
        p3 = Player(user=u3)

        p1.save()
        p2.save()
        p3.save()

        self.assertEqual(len(game.players.all()), 0)

        game.add_player(p1)
        game.add_player(p2)
        game.add_player(p3)

        self.assertEqual(len(game.players.all()), 3)
        self.assertEqual(game.players.all()[0].user.username, "user1")

class PlayerTestCase(TestCase):
    def setUp(self):
        pass

