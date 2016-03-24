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
    name = models.CharField(max_length=64)
    turn_num = models.IntegerField()
    point_num = models.IntegerField()
    author = models.CharField(max_length=32)     # too short?
    file_name = models.CharField(max_length=156, null=True) # length may be too long

    #TODO: make better 
    def __str__(self):
        return self.author + " presents " + self.name

class Character(models.Model):
    name = models.CharField(max_length=64)
    key = models.BooleanField()
    notes = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("edit")

class Location(models.Model):
    name = models.CharField(max_length=64)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("edit")

class Description(models.Model):
    text = models.CharField(max_length=512)
    hidden = models.BooleanField()
    name = models.CharField(max_length=64)
    key = models.BooleanField()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("edit")
        
class Event(models.Model):
    turn = models.IntegerField()

    def __str__(self):
        return "Event on turn "+str(self.turn)

    def get_absolute_url(self):
        return reverese("edit")

class Involved(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        return "Connection between " + str(self.event) + " and " + str(self.character)

    def get_absolute_url(self):
        return reverse("edit")

class HappenedAt(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return "Connection between " + str(self.event) + " and " + str(self.location)
    
    def get_absolute_url(self):
        return reverse("edit")

class DescribedBy(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.ForeignKey(Description, on_delete=models.CASCADE)

    def __str__(self):
        return "Connection between " + str(self.event) + " and " + str(self.description)

    def get_absolute_url(self):
        return reverse("edit")
