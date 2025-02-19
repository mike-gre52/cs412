from django.db import models

# Create your models here.

class Profile(models.Model):

    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.TextField(blank=True)
    image_url = models.TextField(blank=True)

    def __str__(self):
        return f'Name: {self.first_name} {self.last_name}, City: {self.city}, Email: {self.email}'


