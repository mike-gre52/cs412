#mini_fb/models.py
#created by Mike Greene

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    ''' Profile object model'''
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.TextField(blank=True)
    image_url = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mini_fb_profile')

    def __str__(self):
        return f'Name: {self.first_name} {self.last_name}, City: {self.city}, Email: {self.email}'
    
    def get_status_messages(self):
        '''Return a QuerySet to get all status messages about this Profile'''

        status_messages = StatusMessage.objects.filter(profile=self)
        return status_messages
    
    def get_absolute_url(self) -> str:
        '''Returns absolute URL'''
        return reverse('profile', kwargs= {"pk":self.pk})
    
    
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

    def get_friend_suggestions(self):
        ''' A function to get a list of friend suggestions'''
        friends = self.get_friends()
        suggestions = []
        for friend in friends:
            friends_of_friends = friend.get_friends()
            for friend_of_friend in friends_of_friends:
                if friend_of_friend != self and friend_of_friend not in suggestions and friend_of_friend not in friends:
                    suggestions.append(friend_of_friend)
        return suggestions
    
    def get_news_feed(self):
        ''' A function to return all the status messages of this profile and profiles it is friends with'''
        profiles = self.get_friends()
        profiles.append(self)

        status_messages = []
        for profile in profiles:
            status_messages.extend(list(profile.get_status_messages()))
        return sorted(status_messages, key=lambda msg: msg.timestamp, reverse=True)

        

    
class StatusMessage(models.Model):
    ''' StatusMessage object model'''
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def get_images(self):
        status_images = StatusImage.objects.filter(status_message=self)
        print("status images:" , status_images)
        images = []
        for status_image in status_images:
            images.append(status_image.image)
        return images

    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.message} at {self.timestamp}'
    
class Image(models.Model):
    ''' Friend object model'''
    image_file = models.ImageField(blank=True)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    caption = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

class StatusImage(models.Model):
    ''' Status Image object model'''
    image = models.ForeignKey("Image", on_delete=models.CASCADE)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)

class Friend(models.Model):
    ''' Friend object model'''
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Friend object.'''
        return f'{self.profile1.first_name} & {self.profile2.first_name}'