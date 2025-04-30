from django import forms
from .models import Profile, Review, VideoGameList

#project/forms.py
#created by Mike Greene

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''

        model = Profile
        fields = ['first_name', 'last_name', 'email','image_file']

class CreateReviewForm(forms.ModelForm):
    '''A form to add a Profile to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''

        model = Review
        fields = ['message', 'rating']

class CreateVideoGameListForm(forms.ModelForm):
    '''A form to create a videogame list'''
    class Meta:
        model = VideoGameList
        fields = ['name', 'games']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'List Name'}),
            'games': forms.CheckboxSelectMultiple(),
        }

class UpdateReviewForm(forms.ModelForm):
    '''A form to handle an update to an Review'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Review
        fields = ['message', 'rating']