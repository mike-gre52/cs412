from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):

    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.TextField(blank=True)
    image_url = models.TextField(blank=True)

    def __str__(self):
        return f'Name: {self.first_name} {self.last_name}, City: {self.city}, Email: {self.email}'
    
    def get_status_messages(self):
        '''Return a QuerySet to get all status messages about this Profile'''

        status_messages = StatusMessage.objects.filter(profile=self)
        return status_messages
    
    def get_absolute_url(self) -> str:
        return reverse('profile', kwargs= {"pk":self.pk})
    
class StatusMessage(models.Model):

    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.message} at {self.timestamp}'
    



