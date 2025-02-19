from django.shortcuts import render
from django.views.generic import ListView, DetailView #Displays a single instance of one model
from .models import Article
import random

# Create your views here.

class ShowAllView(ListView):
    '''Define a view class to show all blog Articles.'''
    
    model = Article # retrieve objects of type Article from the database
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # how to find the data in the template file

class ArticleView(DetailView):
    '''Display a single article.'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" # Because we are displaying only one article we are using a singular name

class RandomArticleView(DetailView):
    '''Display a single article selected at random.'''



    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" # Because we are displaying only one article we are using a singular name

    #methods
    def get_object(self):
        '''Return one instance of the Article object selected at random.'''

        all_articles = Article.objects.all()
        articles = random.choice(all_articles)
        return articles