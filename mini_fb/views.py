#mini_fb/views.py
#created by Mike Greene

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View #Displays a single instance of one model
from .models import Profile, Image, StatusImage, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
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

        sm = form.save() #Reference to the new StatusMessage object

        files = self.request.FILES.getlist('files') # Read the file from the form

        for file in files:
            image = Image.objects.create(
                image_file = file,
                profile = profile,
            )
            image.save()

            status_image = StatusImage.objects.create(
                image = image,
                status_message = sm,
            )
            status_image.save()

        #delegate the work to the superclass method form_valid:
        return super().form_valid(form)

class UpdateProfileView(UpdateView):
    '''View class to handle update of profile based on its PK.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

class DeleteStatusMessageView(DeleteView):
    '''A view to delete a StatusMessage and remove it from the database.'''

    template_name = "mini_fb/delete_status_message_form.html"
    model = StatusMessage
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''

        # get the pk for this StatusMessage
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.get(pk=pk)
        profile = status_message.profile
        
        # find the article to which this Comment is related by FK
        #article = comment.article
        
        # reverse to show the article page
        return reverse('profile', kwargs={'pk':profile.pk})
    
class UpdateStatusView(UpdateView):
    '''View class to handle update of Status based on its PK.'''

    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_message_form.html"

    def get_context_data(self, ):
        '''Make the profile and status_message available in the template.'''

        context = super().get_context_data()
        context["profile"] = self.object.profile
        context["status_message"] = self.object
        return context
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the update.'''

        # get the pk for this StatusMessage
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.get(pk=pk)
        profile = status_message.profile
        
        # find the article to which this Comment is related by FK
        #article = comment.article
        
        # reverse to show the article page
        return reverse('profile', kwargs={'pk':profile.pk})
    
class AddFriendView(View):
    '''A view to add a friend'''

    def dispatch(self,request, *args, **kwargs):
        '''Add a friend relationship'''
        pk1 = kwargs['pk']
        pk2 = kwargs['other_pk']

        user1 = Profile.objects.get(pk = pk1)
        user2 = Profile.objects.get(pk = pk2)
        user1.add_friend(user2)
        return redirect(self.get_success_url())
        #return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        '''Define a URL to be directed to'''
        pk = self.kwargs.get('pk')
        return reverse('profile', kwargs={'pk':pk})

class ShowFriendSuggestionsView(DetailView):
    '''A view to display friend sugggestions for a specific profile '''

    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile_suggestions'
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data(**kwargs)

        #get friend_suggestions
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context
