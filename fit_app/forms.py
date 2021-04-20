from django import forms
from .models import User, Workout

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")

class WorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ("author", "workout")