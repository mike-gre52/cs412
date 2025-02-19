from django.db import models

# Create your models here.

class Article(models.Model):
    '''Encapsulate the idea of an Article by some author.'''

    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.title} by {self.author}'