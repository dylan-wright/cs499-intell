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
from django.test import Client

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

'''
ProcessActionsTestCase
    used to test action processing
'''
class ProcessActionsTestCase(TestCase):
    def setUp(self):
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

        #fixture scenario
        c = Client()
        file_in = open("editor/static/editor/fixture.json", 'r')
        body = file_in.read()
        file_in.close()
        response = c.post("/editor/accept_ajax_scenario/",
                          content_type="application/json",
                          data=body)
        game = Game(scenario=Scenario.objects.all()[0])
        game.save()
        game.add_player(p1)
        game.add_player(p2)
        game.add_player(p3)
        game.start()
                    

    def test_tail_action(self):
        '''test tail action'''
        game = Game.objects.all()[0]
        ted = Character.objects.get(name="Ted Kaczynski")
        #targeting character ted kazinski
        action = Action(acttype="tail", acttarget=ted.pk)
        action.save()
        #using player 1's 1st agent (only at this point)
        agent = game.players.all()[0].agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

    def test_investigate_action(self):
        '''test investigate action'''
        game = Game.objects.all()[0]
        seattle = Location.objects.get(name="Seattle")
        #targeting location seattle
        action = Action(acttype="investigate", acttarget=seattle.pk)
        action.save()
        #using player 1's 1st agent (only at this point)
        agent = game.players.all()[0].agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

    def test_check_action(self):
        '''test check info action'''
        game = Game.objects.all()[0]
        reserv_cairo = Description.objects.get(text__contains="reservations for Cairo")
        #targeting description "Ata hari makes ...."
        action = Action(acttype="check", acttarget=reserv_cairo.pk)
        action.save()
        #using player 1's 1st agent
        agent = game.players.all()[0].agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

    def test_misinf_action(self):
        '''test create misinf action'''
        game = Game.objects.all()[0]

    def test_recruit_action(self):
        '''test recruit agent action'''
        game = Game.objects.all()[0]
        action = Action(acttype="recruit")
        action.save()
        agent = game.players.all()[0].agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

    def test_apprehend_action(self):
        '''test apprehend character action'''
        game = Game.objects.all()[0]
        ted = Character.objects.get(name="Ted Kaczynski")
        action = Action(acttype="apprehend", acttarget=ted.pk)
        agent = game.players.all()[0].agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

    def test_research_action(self):
        '''test research action'''
        game = Game.objects.all()[0]
        action = Action(acttype="research")
        agent = game.players.all()[0].agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

    def test_terminate__action(self):
        '''test terminate agent action'''
        game = Game.objects.all()[0]
        p2_agent = game.players.all()[1].agent_set.all()[0]
        action = Action(acttype="terminate", target=p2_agent.pk)
        agent = game.players.all()[0].agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)
