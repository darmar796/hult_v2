from django.db import models
from django import forms

# Create your models here.

# class Member(models.Model):
#     firstname = models.CharField(max_length=255)
#     lastname = models.CharField(max_length=255)
#     phone = models.IntegerField(null=True)
#     joined_date = models.DateField(null=True)

class InputForm(forms.Form):
    name = forms.CharField(max_length=100)

class Player(models.Model):
    name = models.CharField(max_length=100)
    game_id = models.CharField(max_length=32, null=True)
    # user_id = models.CharField(max_length=150, null=True)
    user_id = models.IntegerField(null=True)

class Game(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    players = models.ManyToManyField(Player, null=True)

class AddReservation(forms.Form):
    date = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'},  format='%I:%M %p'))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}, format='%I:%M %p'))
