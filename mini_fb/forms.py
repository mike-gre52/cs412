from django import forms
from .models import Profile, StatusMessage

#mini_fb/forms.py
#created by Mike Greene

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''

        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email','image_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a Profile to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        
        model = StatusMessage
        fields = ['message']