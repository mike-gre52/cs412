#mini_fb/views.py
#created by Mike Greene

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView #Displays a single instance of one model
from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse

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

class CreateProfileView(CreateView):
    '''A view to create a new Profile and save it to the database.'''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''

        return self.object.get_absolute_url()

class CreateStatusMessageView(CreateView):
    '''A view to create a new StatusMessage and save it to the database.'''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all')
        pk = self.kwargs['pk']
        return reverse('profile', kwargs={'pk':pk})

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add this profile into the context dictionary:
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Comment
        object before saving it to the database.
        '''

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        #attach this profile to the comment
        form.instance.profile = profile # Set the Foreign Key

        #delegate the work to the superclass method form_valid:
        return super().form_valid(form)


