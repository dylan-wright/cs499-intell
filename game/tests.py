'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell/
        https://intellproject.com/

        /game/tests.py
            Django TestCase's 
                GameTestCase
                    test_start_next_turn
                    test_games_init
                    test_add_player
                    test_start_game
                PlayerTestCase
                    test_create_player

        TODO: add other model test cases
        TODO: add routing/templates/view test cases
        TODO: add documentation for which test maps to which TestCase
'''
from django.test import TestCase
from .models import *
from editor.models import Scenario
from django.contrib.auth.models import User

# Create your tests here.
'''
GameTestCase
    used to test game model
        test_start_next_turn
        test_games_init
        test_add_player
        test_start_game
'''
class  GameTestCase(TestCase):
    def setUp(self):
        Scenario.objects.create(name="test",
                                turn_num=20,
                                point_num=20,
                                author="test",
                                file_name="fixture.json")
        Game.objects.create(scenario=Scenario.objects.all()[0])

    def test_start_next_turn(self):
        '''test turn timing function works'''
        game = Game.objects.get(pk=1)
        
        self.assertEqual(game.started, False)
        next_turn = game.next_turn
        self.assertEqual(next_turn, None)

        #start game
        game.start()
        self.assertEqual(game.started, True)
        self.assertNotEqual(game.next_turn, next_turn)

        next_turn = game.next_turn

        self.assertEqual(game.turn, 1)
        game.start_next_turn()
        self.assertEqual(game.turn, 2)
        self.assertNotEqual(game.next_turn, next_turn)

        next_turn = game.next_turn

        self.assertEqual(game.turn, 2)
        game.start_next_turn()
        self.assertEqual(game.turn, 3)
        self.assertNotEqual(game.next_turn, next_turn)
        self.assertEqual(game.next_turn, next_turn+game.turn_length)

    def test_games_init(self):
        '''test game initialized'''
        game = Game.objects.get(pk=1)
        scenario = game.scenario
        
        self.assertEqual(scenario.name, "test")
        self.assertEqual(scenario.turn_num, 20)
        self.assertEqual(scenario.point_num, 20)
        self.assertEqual(scenario.author, "test")
        self.assertEqual(scenario.file_name, "fixture.json")
        self.assertEqual(game.started, False)

    def test_add_player(self):
        '''test that a user can only join a game once'''
        game = Game.objects.get(pk=1)

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

        game.add_player(p1)
        game.add_player(p2)
        game.add_player(p2)

        self.assertEqual(len(game.players.all()), 3)

    def test_start_game(self):
        '''test games start correctly'''
        game = Game.objects.get(pk=1)

        game.start()
        self.assertEqual(game.started, True)
'''
PlayerTestCase
    used to test Player model
        test_create_player
'''
class PlayerTestCase(TestCase):
    def setUp(self):
        u1 = User(username="user1", first_name="Test 1")
        u1.save()
    
    def test_create_player(self):
        '''test creating player'''
        player = Player(user=User.objects.get(username="user1"))
        player.save()

        self.assertEqual(len(Player.objects.all()), 1)
        self.assertEqual(player.user.username, "user1")
