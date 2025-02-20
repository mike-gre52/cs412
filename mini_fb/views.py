from django.shortcuts import render
from django.views.generic import ListView, DetailView #Displays a single instance of one model
from .models import Profile

# Create your views here.

class ShowAllProfilesView(ListView):
    '''Defines a view class to show all profiles'''
    
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    ''' Defines a view class to show a sinlge profile '''

    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'