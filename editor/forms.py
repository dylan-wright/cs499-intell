from django import forms
from .models import *

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('turn',)

class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ('text', 'hidden', 'key', 'name')

class DescribedByForm(forms.ModelForm):
    class Meta:
        model = DescribedBy
        fields = ('event', 'description')

class HappenedAtForm(forms.ModelForm):
    class Meta:
        model = HappenedAt
        fields = ('event', 'location')

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'key', 'notes')

class InvolvedForm(forms.ModelForm):
    class Meta:
        model = Involved
        fields = ('event', 'character')

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'x', 'y')
