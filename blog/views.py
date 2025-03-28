from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView #Displays a single instance of one model
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW
from django.urls import reverse

import random

# Create your views here.

class ShowAllView(ListView):
    '''Define a view class to show all blog Articles.'''
    
    model = Article # retrieve objects of type Article from the database
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # how to find the data in the template file

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')

        return super().dispatch(request, *args, **kwargs)

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
    

class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Article.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
            '''
            Handle the form submission to create a new Article object.
            '''
            print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')

            # find the logged in user
            user = self.request.user
            print(f"CreateArticleView user={user} article.user={user}")

            # attach user to form instance (Article object):
            form.instance.user = user

            return super().form_valid(form)
            


class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all')
        pk = self.kwargs['pk']
        return reverse('article', kwargs={'pk':pk})

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['article'] = article
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment
        object before saving it to the database.
        '''

        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        #attach this article to the comment
        form.instance.article = article # Set the Foreign Key

        #delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    

class UpdateArticleView(UpdateView):
    '''View class to handle update of an article based on its PK.'''

    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"


class DeleteCommentView(DeleteView):
    '''A view to delete a comment and remove it from the database.'''

    template_name = "blog/delete_comment_form.html"
    model = Comment
    context_object_name = 'comment'
    
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''

        # get the pk for this comment
        pk = self.kwargs.get('pk')
        comment = Comment.objects.get(pk=pk)
        
        # find the article to which this Comment is related by FK
        article = comment.article
        
        # reverse to show the article page
        return reverse('article', kwargs={'pk':article.pk})
    
class RegistrationView(CreateView):
    '''
    show/process form for account registration
    '''

    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User
    
    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')