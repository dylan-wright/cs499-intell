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
                ProcessActionTestCase
                    test_tail_action
                    test_investigate_action
                    test_check_action
                    test_misinf_action <- not implemented
                    test_recruit_action
                    test_apprehend_action
                    test_research_action
                    test_terminate_action

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
        test_tail_action
        test_investigate_action
        test_check_action
        test_misinf_action <- not implemented
        test_recruit_action
        test_apprehend_action
        test_research_action
        test_terminate_action
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
        player = game.players.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)
        
        #check that points deducted correctly
        #first turn involving ted is 9
        game.turn = 9
        game.save()

        point_count = player.points
        knowledge_count = len(player.get_knowledge())
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points, 
                         point_count-game.ACTION_COSTS["tail"])
        #new knowledge?
        self.assertNotEqual(len(player.get_knowledge()), knowledge_count)

        game.turn = 0
        game.save()

        #create a character not in the scenario
        michael = Character(name="Michael", key=False, notes="")
        michael.save()
        action.acttarget = michael.pk
        action.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, False)

    def test_tail_succeed(self):
        '''test a tail action that finds a hidden description'''
        #add target event/descriptions/character
        d_public = Description(name="public description",
                               text="Anyone can see this",
                               key=True,
                               hidden=False)
        d_public.save()
        d_private = Description(name="private description",
                                text="Must tail character/investigate location",
                                key=True,
                                hidden=True)
        d_private.save()

        event = Event(turn=0, scenario=Scenario.objects.all()[0], misinf=False)
        event.save()

        db_public = DescribedBy(event=event, description=d_public)
        db_public.save()
        db_private = DescribedBy(event=event, description=d_private)
        db_public.save()

        character = Character(name="Follow Me", key=True, notes="")
        character.save()

        involved = Involved(event=event, character=character)
        involved.save()

        #try to investigate
        game = Game.objects.all()[0]
        action = Action(acttype="tail", acttarget=character.pk)
        action.save()
        player = game.players.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        
        #sanity check (other test should cover this)
        self.assertEqual(game.is_target_valid(action), True)

        #check that knowledge and message objects created
        pre_knowledge = len(player.get_knowledge())
        pre_messages = len(player.get_messages())

        game.perform_action(action)
        
        player.refresh_from_db()

        post_knowledge = len(player.get_knowledge())
        post_messages = len(player.get_messages())

        self.assertEqual(pre_knowledge+1, post_knowledge)
        self.assertEqual(pre_messages+1, post_messages)

    def test_investigate_action(self):
        '''test investigate action'''
        game = Game.objects.all()[0]
        seattle = Location.objects.get(name="Seattle")
        #targeting location seattle
        action = Action(acttype="investigate", acttarget=seattle.pk)
        action.save()
        #using player 1's 1st agent (only at this point)
        player = game.players.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

        #check that points deducted correctly
        #first seattle turn is 7
        game.turn = 8
        game.save()

        point_count = player.points
        knowledge_count = len(player.get_knowledge())
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points, 
                         point_count-game.ACTION_COSTS["investigate"])
        #new knowledge?
        self.assertNotEqual(len(player.get_knowledge()), knowledge_count)

        game.turn = 0
        game.save()

        #create a location not in the scenario
        moon = Location(name="The Moon", x=0, y=0)
        moon.save()
        action.acttarget = moon.pk
        action.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, False)
    
    def test_investigate_succeed(self):
        '''test an investigate action that finds a hidden description'''
        #add target event/descriptions/character
        d_public = Description(name="public description",
                               text="Anyone can see this",
                               key=True,
                               hidden=False)
        d_public.save()
        d_private = Description(name="private description",
                                text="Must tail character/investigate location",
                                key=True,
                                hidden=True)
        d_private.save()

        event = Event(turn=0, scenario=Scenario.objects.all()[0], misinf=False)
        event.save()

        db_public = DescribedBy(event=event, description=d_public)
        db_public.save()
        db_private = DescribedBy(event=event, description=d_private)
        db_public.save()

        location = Location(name="Look here", x=0,y=0)
        location.save()

        happenedat = HappenedAt(event=event, location=location)
        happenedat.save()

        #try to investigate
        game = Game.objects.all()[0]
        action = Action(acttype="investigate", acttarget=location.pk)
        action.save()
        player = game.players.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        
        #sanity check (other test should cover this)
        self.assertEqual(game.is_target_valid(action), True)

        #check that knowledge and message objects created
        pre_knowledge = len(player.get_knowledge())
        pre_messages = len(player.get_messages())

        game.perform_action(action)
        
        player.refresh_from_db()

        post_knowledge = len(player.get_knowledge())
        post_messages = len(player.get_messages())

        self.assertEqual(pre_knowledge+1, post_knowledge)
        self.assertEqual(pre_messages+1, post_messages)

    def test_check_action(self):
        '''test check info action'''
        game = Game.objects.all()[0]
        reserv_cairo = Description.objects.get(text__contains="reservations for Cairo")
        #targeting description "Ata hari makes ...."
        action = Action(acttype="check", acttarget=reserv_cairo.pk)
        action.save()
        #using player 1's 1st agent
        player = game.players.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

        #check that points deducted correctly
        point_count = player.points
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points, 
                         point_count-game.ACTION_COSTS["check"])

        #create a description not in the scenario
        jogging = Description(text="Someone went jogging", hidden=False,
                              name="Jogging", key=False)
        jogging.save()
        action.acttarget = jogging.pk
        action.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, False)

    def test_check_succeed(self):
        '''test check action finds bogus info'''
        description = Description(name="bad info",
                                  key=False,
                                  hidden=False,
                                  text="This is bs")
        description.save()

        character = Character.objects.get(name="Ted Kaczynski")
        location = Location.objects.get(name="Seattle")

        event = Event(turn=0, scenario=Scenario.objects.all()[0], misinf=True)
        event.save()

        describedby = DescribedBy(event=event, description=description)
        happenedat = HappenedAt(event=event, location=location)
        involved = Involved(event=event, character=character)
        describedby.save()
        happenedat.save()
        involved.save()
        
        #try to check
        game = Game.objects.all()[0]
        action = Action(acttype="check", acttarget=description.pk)
        action.save()
        player = game.players.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        
        #sanity check (other test should cover this)
        self.assertEqual(game.is_target_valid(action), True)

        #check that knowledge and message objects created
        pre_knowledge = len(player.get_knowledge())
        pre_messages = len(player.get_messages())

        game.perform_action(action)
        
        player.refresh_from_db()

        post_knowledge = len(player.get_knowledge())
        post_messages = len(player.get_messages())

        self.assertEqual(pre_knowledge+1, post_knowledge)
        self.assertEqual(pre_messages+1, post_messages)


    def test_misinf_action(self):
        '''test create misinf action'''
        game = Game.objects.all()[0]
        player = game.players.all()[0]
        agent = player.agent_set.all()[0]
        self.assertEqual(True, False)

        #check that points deducted correctly
        point_count = player.points
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points, 
                         point_count-game.ACTION_COSTS["misinf"])

    def test_recruit_action(self):
        '''test recruit agent action'''
        game = Game.objects.all()[0]
        action = Action(acttype="recruit")
        action.save()
        player = game.players.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

        #test that player has an additional agent after performing action
        agent_count = len(player.agent_set.all())
        game.perform_action(action)
        self.assertEqual(len(player.agent_set.all()), 
                         agent_count+1)
        #check that points deducted correctly
        point_count = player.points
        player.refresh_from_db()
        self.assertEqual(player.points, 
                         point_count-game.ACTION_COSTS["recruit"])


    def test_apprehend_action(self):
        '''test apprehend character action'''
        game = Game.objects.all()[0]
        ted = Character.objects.get(name="Ted Kaczynski")
        action = Action(acttype="apprehend", acttarget=ted.pk)
        action.save()
        player = game.players.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)
        
        #check that points deducted correctly
        point_count = player.points
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points, 
                         point_count-game.ACTION_COSTS["apprehend"])
        
        #create a character not in the scenario
        michael = Character(name="Michael", key=False, notes="")
        michael.save()
        action.acttarget = michael.pk
        action.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, False)

    def test_research_action(self):
        '''test research action'''
        game = Game.objects.all()[0]
        action = Action(acttype="research")
        action.save()
        player = game.players.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)

        #test that the player has additionalk points after performing action
        point_count = player.points
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points, 
                         point_count-game.ACTION_COSTS["research"])

    def test_terminate__action(self):
        '''test terminate agent action'''
        game = Game.objects.all()[0]
        p2_agent = game.players.all()[1].agent_set.all()[0]
        action = Action(acttype="terminate", acttarget=p2_agent.pk)
        action.save()
        player = game.players.all()[0]
        agent = player.agent_set.all()[0]
        agent.action = action
        agent.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, True)
    
        #check that points deducted correctly
        point_count = player.points
        game.perform_action(action)
        player.refresh_from_db()
        self.assertEqual(player.points, 
                         point_count-game.ACTION_COSTS["terminate"])

        #create agent not belonging to a player
        dummy_action = Action(acttype="research")
        dummy_action.save()
        agent = Agent(name="", action=dummy_action)
        agent.save()
        action.acttarget = agent.pk
        action.save()
        valid = game.is_target_valid(action)
        self.assertEqual(valid, False)
