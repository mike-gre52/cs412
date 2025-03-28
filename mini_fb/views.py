#mini_fb/views.py
#created by Mike Greene

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View #Displays a single instance of one model
from .models import Profile, Image, StatusImage, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from django.contrib.auth.forms import UserCreationForm


#class CustomLoginRequiredMixin(LoginRequiredMixin):



# Create your views here.

class ShowAllProfilesView(ListView):
    '''Defines a view class to show all profiles'''
    
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["profile"] = Profile.objects.get(user = self.request.user)
        return context

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
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)  
        context["user_create_form"] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        '''Process valid form submission.'''
        user_create_form = UserCreationForm(self.request.POST)  # Recreate UserCreationForm

        # if valid save a new user and continue with super method
        if user_create_form.is_valid():
            user = user_create_form.save() 

            form.instance.user = user 
            return super().form_valid(form) 
        
        # If user form is not valid, re-render the page with errors
        return self.render_to_response(self.get_context_data(form=form, user_create_form=user_create_form))


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to create a new StatusMessage and save it to the database.'''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all')
        pk = Profile.objects.get(user = self.request.user).pk
        return reverse('profile', kwargs={'pk':pk})

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        profile = Profile.objects.get(user = self.request.user)

        # add this profile into the context dictionary:
        context['profile'] = profile
        return context
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Comment
        object before saving it to the database.
        '''

        profile = Profile.objects.get(user = self.request.user)

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
    
    def get_object(self):
        return Profile.objects.get(user = self.request.user)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''View class to handle update of profile based on its PK.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["profile"] = Profile.objects.get(user = self.request.user)
        return context

    def get_object(self):
        return Profile.objects.get(user = self.request.user)

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''A view to delete a StatusMessage and remove it from the database.'''

    template_name = "mini_fb/delete_status_message_form.html"
    model = StatusMessage
    context_object_name = 'status_message'

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["profile"] = Profile.objects.get(user = self.request.user)
        return context

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
    
class UpdateStatusView(LoginRequiredMixin, UpdateView):
    '''View class to handle update of Status based on its PK.'''

    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_message_form.html"

    def get_context_data(self, ):
        '''Make the profile and status_message available in the template.'''

        context = super().get_context_data()


        if self.request.user.is_authenticated:
            context["profile"] = Profile.objects.get(user = self.request.user)
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
    
class AddFriendView(LoginRequiredMixin, View):
    '''A view to add a friend'''

    def dispatch(self,request, *args, **kwargs):
        '''Add a friend relationship'''
        pk2 = kwargs['other_pk']

        user1 = Profile.objects.get(user = self.request.user)
        user2 = Profile.objects.get(pk = pk2)
        user1.add_friend(user2)
        return redirect(self.get_success_url())
        #return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        '''Define a URL to be directed to'''
        user = Profile.objects.get(user = self.request.user)
        pk = user.pk
        return reverse('profile', kwargs={'pk':pk})

    def get_object(self):
        return Profile.objects.get(user = self.request.user)

    

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    '''A view to display friend sugggestions for a specific profile '''

    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile_suggestions'

    def get_object(self):
        return Profile.objects.get(user = self.request.user)
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data(**kwargs)

            
        if self.request.user.is_authenticated:
            context["profile"] = Profile.objects.get(user = self.request.user)
        return context

        #get friend_suggestions
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    '''A View to display the newsfeed for a profile'''

    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'news_feed'

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data(**kwargs)


        if self.request.user.is_authenticated:
            context["profile"] = Profile.objects.get(user = self.request.user)
        #get friend_suggestions
        context['news_feed'] = self.object.get_news_feed()
        return context

    def get_object(self):
        return Profile.objects.get(user = self.request.user)