from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

#Created by Mike Greene

# Create your models here.

class Profile(models.Model):
    '''Profile object Model'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    email = models.TextField(blank=True)
    image_file = models.ImageField(blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        ''' function to get absolute url'''
        return reverse('profile', kwargs= {"pk":self.pk})

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'Name: {self.first_name} {self.last_name}, Email: {self.email}, Join Date: {self.join_date}'
    
    def get_friends(self):
        ''' A function to get all friends of the profile self'''
        friends = []
        #add profile to friends list from profile2
        friendsQueryList = list(Friend.objects.filter(profile1=self))
        for friend in friendsQueryList:
            friends.append(friend.profile2)

        #add profile to friends list from profile1
        friendsQueryList = list(Friend.objects.filter(profile2=self))
        for friend in friendsQueryList:
            friends.append(friend.profile1)
        return friends
    
    def get_favorite_video_games(self):
         ''' A function to get all favorite video games of the profile self'''
         return list(FavoriteVideoGame.objects.filter(profile=self))

    def add_friend(self, other):
        ''' A function to create a friend relationship between self and other'''
        #Check if self and other are not the same user
        if self == other:
            print("cannot friend youself")
            return

        #Check if self and other are not already friends
        friends = self.get_friends()
        if other in friends: 
            print("already friends")
            return

        #Create new Friend Object
        friend = Friend.objects.create(profile1=self, profile2=other)
        friend.save()

    def add_favorite_game(self, game):
        ''' function to add FavoriteVideoGame object tied to this profile'''
        favorite = FavoriteVideoGame.objects.create(profile = self, video_game = game)
        favorite.save()

    
class VideoGame(models.Model):
    '''VideoGame object Model'''
    title = models.TextField(blank=True)
    developer = models.TextField(blank=True)
    release_date = models.DateField()
    genre = models.TextField(blank=True)
    cover_image = models.TextField(blank=True)
    description = models.TextField(blank=True)
    platforms = models.TextField(blank=True)

    def __str__(self):
        '''Return a string representation of this VideoGame object.'''
        return f'{self.title} {self.developer}'
    
class FavoriteVideoGame(models.Model):
    '''FavoriteVideoGame object Model'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    video_game = models.ForeignKey(VideoGame, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this FavoriteVideoGame object.'''
        return f'{self.profile.first_name} {self.profile.last_name} favorited {self.video_game.title}'
    
class Review(models.Model):
    '''Review object Model'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    video_game = models.ForeignKey(VideoGame, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    rating = models.IntegerField(default=1,validators=[MaxValueValidator(100), MinValueValidator(1)])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this Review object.'''
        return f"Review of {self.video_game.title} by {self.profile.first_name} {self.profile.last_name} with a score of {self.rating}"
    
    def get_reviews_from_game(game):
        ''' A function to get all reviews for a game'''
        return list(Review.objects.filter(video_game=game).order_by('-timestamp'))
    
    def get_reviews_from_profile(profile):
        ''' A function to get all reviews for a game'''
        return list(Review.objects.filter(profile=profile))


    
class Friend(models.Model):
    '''Friend object model'''
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this Friend object.'''
        return f'{self.profile1.first_name} & {self.profile2.first_name}'

class VideoGameList(models.Model):
    ''' VideoGameList object model'''
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    name = models.TextField(blank=True)
    games = models.ManyToManyField(VideoGame)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        ''' override string method'''
        return f"{self.profile.first_name}'s List of {self.games}"



