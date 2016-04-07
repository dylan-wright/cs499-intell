'''
    INTELL The Craft of Intelligence
    Django Models - Scenario Database schema design:
            https://intellproject.com/~dylan/INTELL/documents/schema.shtml
            TODO: this ^

    Version
        0314 :  Incorporated prototype models
        0324 :  Start migration to FE centric editor with verification BE
                Added Scenario Model
'''

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
'''
Scenario
    id          - auto gen primary key
    name        - author's name for scenario
    turn_num    - turns in game
    author      - author's name, db will actually connect author model to
                    their scenarios but this way the author can choose to
                    be anonomys - thats not spelled right sue me. 
    file_name   - location JSON dump will be stored (/static ?)
'''
class Scenario(models.Model):
    name = models.CharField(max_length=64, null=True)
    turn_num = models.IntegerField()
    point_num = models.IntegerField()
    author = models.CharField(max_length=32)     # too short?
    file_name = models.FileField(upload_to='scenarios', null=True) 
    events = models.ForeignKey('Event', null=True)

    def __str__(self):
        return self.author + " presents " + self.name

    '''
    load_events
        used to populate db if the events in the file are not in the db
        called when a game is being spun up
        for now unimplemnted (events always in db)
    '''
    def load_events(self):
        pass

    '''
    unload_events
        used to depopulate db when a game ends. 
        called by manager
        for now unimplemented (events always in db)
    '''
    def unload_events(self):
        pass

'''
Character
    id          - auto get primary key
    name        - name of character
    key         - is the character key to the scenario? True: user wins on
                    capture
    notes       - author notes about character
'''
class Character(models.Model):
    name = models.CharField(max_length=64)
    key = models.NullBooleanField()
    notes = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("edit")

'''
Location
    id          - auto gen primary key
    name        - name of location
    x           - x coord of location
    y           - y coord of location
'''
class Location(models.Model):
    name = models.CharField(max_length=64)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("edit")

'''
Description
    id          - auto gen primary key
    text        - description of the event (events can have multiple
                    description so multiple text's)
    hidden      - flag indicating whether the description is hidden by default
                    an Event's Description(s) can have different hidden flag
                    values (basis of investigations)
    name        - TODO:why does this have a name
    key         - flag indicating if the description is relevent to the
                    scenario 
                    TODO: should this be moved to event? (i say no)
'''
class Description(models.Model):
    text = models.CharField(max_length=512)
    hidden = models.BooleanField()
    name = models.CharField(max_length=64)
    key = models.NullBooleanField()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("edit")
        
'''
Event
    id          - auto gen primary key
    turn        - turn event occurs on
'''
class Event(models.Model):
    turn = models.IntegerField()

    def __str__(self):
        return "Event on turn "+str(self.turn)

    def get_absolute_url(self):
        return reverese("edit")

'''
Involved
    id          - auto gen primary key
    event       - id of event
    character   - id of character
'''
class Involved(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        return "Connection between " + str(self.event) + " and " + str(self.character)

    def get_absolute_url(self):
        return reverse("edit")

'''
HappenedAt
    id          - auto gen primary key
    event       - id of event
    location    - id of location
'''
class HappenedAt(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return "Connection between " + str(self.event) + " and " + str(self.location)
    
    def get_absolute_url(self):
        return reverse("edit")

'''
DescribedBy
    id          - auto gen primary key
    event       - id of event
    description - id of description
'''
class DescribedBy(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.ForeignKey(Description, on_delete=models.CASCADE)

    def __str__(self):
        return "Connection between " + str(self.event) + " and " + str(self.description)

    def get_absolute_url(self):
        return reverse("edit")
