from django.shortcuts import render, redirect


from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from .models import Profile, VideoGame, Friend, Review, VideoGameList, FavoriteVideoGame
from .forms import CreateProfileForm, CreateReviewForm, CreateVideoGameListForm, UpdateReviewForm
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm

#Created by Mike Greene

# Create your views here.

class ShowAllProfilesView(ListView):
    '''Defines a view class to show all profiles'''
    
    model = Profile
    template_name = 'project/show_all_profiles.html'
    context_object_name = 'profiles'

    #def get_context_data(self, **kwargs):
    #    '''Return the dictionary of context variables for use in the template.'''
    #    context = super().get_context_data(**kwargs)
    #    if self.request.user.is_authenticated:
    #        context["profile"] = Profile.objects.get(user = self.request.user)
    #    return context

class ShowProfilePageView(DetailView):
    ''' Defines a view class to show a single profile '''

    model = Profile
    template_name = 'project/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data(**kwargs)

        context['reviews'] = Review.get_reviews_from_profile(self.object)
        return context


class ShowAllVideoGames(ListView):
    '''Defines a view class to show all Videogames'''
    
    model = VideoGame
    template_name = 'project/show_all_videogames.html'
    context_object_name = 'videogames'
            
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data(**kwargs)
        context['years'] = list(reversed(range(1970, 2025)))
        return context

    def get_queryset(self):
        ''' filters the video games based on form submission'''
        #Filter the voter query

        #all voters
        games = super().get_queryset()
   
        #filter party
        if 'genre' in self.request.GET:
            genre = self.request.GET['genre'].strip()
            if genre and genre != "Any":
                print(genre, "filtering")
                games = games.filter(genre=genre)
        
        #filter min_date
        if 'min_date' in self.request.GET:
            min_date = self.request.GET['min_date']
            if min_date != "Any":
                min_date = min_date + '-01-01'
                min_date = datetime.strptime(min_date, '%Y-%m-%d').date()
                
                games = games.filter(release_date__gt=min_date)
        
        #filter max_dob
        if 'max_date' in self.request.GET:
            max_date = self.request.GET['max_date']
            if max_date != "Any":
                max_date = max_date + '-01-01'
                max_date = datetime.strptime(max_date, '%Y-%m-%d').date()
                
                games = games.filter(release_date__lt=max_date)

        return games
        
  

class ShowVideoGamePageView(DetailView):
    ''' Defines a view class to show a single profile '''

    model = VideoGame
    template_name = 'project/show_video_game.html'
    context_object_name = 'videogame'

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.get_reviews_from_game(self.object)
        return context
    
class ShowAllReviews(ListView):
    '''Defines a view class to show all Videogames'''
    
    model = Review
    template_name = 'project/show_all_reviews.html'
    context_object_name = 'reviews'
    
    def get_queryset(self):
        '''Override the default queryset to order by the Review attribute 'timestamp' '''
        return Review.objects.all().order_by('-timestamp')

class CreateProfileView(CreateView):
    '''A view to create a new Profile and save it to the database.'''

    form_class = CreateProfileForm
    template_name = "project/create_profile_form.html"

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''

        return self.object.get_absolute_url()
    
    # def get_context_data(self, **kwargs):
    #     '''Return the dictionary of context variables for use in the template.'''
    #     context = super().get_context_data(**kwargs)  
    #     context["user_create_form"] = UserCreationForm()
    #     return context
    
    # def form_valid(self, form):
    #     '''Process valid form submission.'''
    #     user_create_form = UserCreationForm(self.request.POST)  # Recreate UserCreationForm

    #     # if valid save a new user and continue with super method
    #     if user_create_form.is_valid():
    #         user = user_create_form.save() 

    #         form.instance.user = user 
    #         return super().form_valid(form) 
        
    #     # If user form is not valid, re-render the page with errors
    #     return self.render_to_response(self.get_context_data(form=form, user_create_form=user_create_form))

class CreateReviewView(CreateView):
    ''' View to create a Review'''
    model = Review 
    form_class = CreateReviewForm
    template_name = 'project/add_review.html'

    def form_valid(self, form):
        ''' Validates the form is valid'''
        profile_pk = self.kwargs['profile_pk']
        favorite_game_pk = self.kwargs['game_pk']

        profile = Profile.objects.get(pk = profile_pk)
        game = FavoriteVideoGame.objects.get(pk = favorite_game_pk).video_game

        form.instance.profile = profile
        form.instance.video_game = game
        return super().form_valid(form)

    def get_success_url(self):
        # After submitting, go back to the profile page (for example)
        return reverse('profile', kwargs={'pk': self.kwargs['profile_pk']})
    
class SelectProfileToAdd(ListView):
    '''Defines a view class to show all profiles'''
    
    model = Profile
    template_name = 'project/add_friend.html'
    context_object_name = 'profiles'
    
    def get_queryset(self):
        ''' Filters profiles viewable'''
        # Exclude the current user profile from the list
        return Profile.objects.exclude(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        ''' context for the view'''
        context = super().get_context_data(**kwargs)
        # Get the profile_pk from the URL kwargs
        context['current_profile_pk'] = self.kwargs.get('profile_pk')
        print("sdlkfjlkdsjf", self.kwargs.get('profile_pk'))
        return context

class AddFriendView(View):
    '''A view to add a friend'''

    def dispatch(self,request, *args, **kwargs):
        '''Add a friend relationship'''
        pk1 = kwargs['profile_pk']
        pk2 = kwargs['friend_pk']

        user1 = Profile.objects.get(pk = pk1)
        user2 = Profile.objects.get(pk = pk2)
        user1.add_friend(user2)
        return redirect(self.get_success_url())

    def get_success_url(self):
        '''Define a URL to be directed to'''
        user = Profile.objects.get(pk = self.kwargs.get('profile_pk'))
        pk = user.pk
        return reverse('profile', kwargs={'pk':pk})

    def get_object(self):
        ''' function to obtain object to add'''
        return Profile.objects.get(user = self.request.user)
    
class SelectVideoGameToAdd(ListView):
    '''Defines a view class to show all Games'''
    
    model = VideoGame
    template_name = 'project/add_game.html'
    context_object_name = 'videogames'
    
    #def get_queryset(self):
        # Exclude the current user profile from the list
        #return Profile.objects.exclude(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        ''' context for SelectVideoGameToAdd View'''
        context = super().get_context_data(**kwargs)
        # Get the profile_pk from the URL kwargs
        context['profile_pk'] = self.kwargs.get('profile_pk')
        return context
    
class AddFavoriteGameView(View):
    '''A view to add a favorite game'''

    def dispatch(self,request, *args, **kwargs):
        '''Add a favorite game'''
        profile_pk = kwargs['profile_pk']
        game_pk = kwargs['game_pk']

        user = Profile.objects.get(pk = profile_pk)
        game = VideoGame.objects.get(pk = game_pk)
        user.add_favorite_game(game)
        return redirect(self.get_success_url())

    def get_success_url(self):
        '''Define a URL to be directed to'''
        user = Profile.objects.get(pk = self.kwargs.get('profile_pk'))
        pk = user.pk
        return reverse('profile', kwargs={'pk':pk})

    def get_object(self):
        ''' function to get profile of the view'''
        return Profile.objects.get(user = self.request.user)
    
class CreateProfileView(CreateView):
    '''A view to create a new Profile and save it to the database.'''

    form_class = CreateProfileForm
    template_name = "project/create_profile_form.html"
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''

        return self.object.get_absolute_url()
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)  
        context["user_create_form"] = UserCreationForm()
        return context
    
    def get_absolute_url(self):
        ''' function to return absolute url'''
        return reverse('profile', kwargs={'pk': self.pk})
    
    def form_valid(self, form):
        ''' function to validate form on submission'''
        user_create_form = UserCreationForm(self.request.POST, self.request.FILES)

        if user_create_form.is_valid():
            user = user_create_form.save()
            form.instance.user = user
            return super().form_valid(form)

        return self.render_to_response(self.get_context_data(form=form, user_create_form=user_create_form))
    
class VideoGameListsView(ListView):
    '''View to display all VideoGameLists'''
    
    model = VideoGameList
    template_name = 'project/videogame_lists.html'
    context_object_name = 'videogame_lists'
    ordering = ['-timestamp']

    def get_queryset(self):
            ''' filter video games by profile'''
            return VideoGameList.objects.filter(profile = self.kwargs.get('profile_pk'))

    def get_context_data(self, **kwargs):
        ''' Context for videogame list view'''
        context = super().get_context_data(**kwargs)
        # Get the profile_pk from the URL kwargs
        pk = self.kwargs.get('profile_pk')
        context['profile'] = Profile.objects.get(pk = pk)
        return context

    
class CreateVideoGameList(CreateView):
    '''View to display VideoGameList CreateView'''

    model = VideoGameList
    form_class = CreateVideoGameListForm
    template_name = 'project/create_videogamelist.html'

    def form_valid(self, form):
        ''' function to validate form on submission'''
        profile = Profile.objects.get(pk=self.kwargs['profile_pk'])
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        '''function to return a success url'''
        return reverse('videogame_lists', kwargs={'profile_pk': self.kwargs['profile_pk']})
    
class EditReivewView(UpdateView):
    '''View to Update a Review'''

    model = Review
    form_class = UpdateReviewForm
    template_name = 'project/edit_review.html'

    def get_object(self):
        ''' function to obtain review to edit'''
        return Review.objects.get(pk=self.kwargs['review_pk'])

    def get_success_url(self):
        '''Define a URL to be directed to'''
        user = Profile.objects.get(pk = self.kwargs.get('pk'))
        pk = user.pk
        return reverse('profile', kwargs={'pk':pk})
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["profile"] = Profile.objects.get(user = self.request.user)
        return context
    

class DeleteReviewView(DeleteView):
    '''A view to delete a Review and remove it from the database.'''

    template_name = "project/delete_review.html"
    model = Review
    context_object_name = 'review'

    def get_object(self):
        ''' function to return review to be deleted'''
        return Review.objects.get(pk=self.kwargs['review_pk'])

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["profile"] = Profile.objects.get(user = self.request.user)
        return context

    def get_success_url(self):
        '''Define a URL to be directed to'''
        user = Profile.objects.get(pk = self.kwargs.get('pk'))
        pk = user.pk
        return reverse('profile', kwargs={'pk':pk})
    
class DeleteVideoGameListView(DeleteView):
    '''A view to delete a VideoGameList and remove it from the database.'''

    template_name = "project/delete_videogame_list.html"
    model = VideoGameList
    context_object_name = 'game_list'

    def get_object(self):
        ''' Funtion to obtain VideoGameList to be deleted'''
        return VideoGameList.objects.get(pk=self.kwargs['list_pk'])

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["profile"] = Profile.objects.get(user = self.request.user)
        return context

    def get_success_url(self):
        '''Define a URL to be directed to'''
        user = Profile.objects.get(pk = self.kwargs.get('pk'))
        pk = user.pk
        return reverse('profile', kwargs={'pk':pk})