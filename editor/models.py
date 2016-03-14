'''
    INTELL The Craft of Intelligence
    Django Models

    Version
        0314 :  Incorporated prototype models
'''

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Character(models.Model):
    name = models.CharField(max_length=64)
    key = models.BooleanField()
    notes = models.CharField(max_length=512)

    def __str__(self):
        return name

    def get_absolute_url(self):
        return reverse("edit")

class Location(models.Model):
    name = models.CharField(max_length=64)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return name

    def get_absolute_url(self):
        return reverse("edit")

class Description(models.Model):
    text = models.CharField(max_length=512)
    hidden = models.BooleanField()
    name = models.CharField(max_length=64)
    key = models.BooleanField()

    def __str__(self):
        return text

    def get_absolute_url(self):
        return reverse("edit")
        
class Event(models.Model):
    turn = models.IntegerField()

    def __str__(self):
        return "Event on turn "+str(turn)

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
