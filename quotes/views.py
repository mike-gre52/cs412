from django.shortcuts import render

import random

# Create your views here.

quotes = [
    "If silence seems to give approval, then remaining silent is cowardly.",
    "Democracy requires both discipline and hard work. It is not easy for individuals to govern themselves. . . . It is one thing to gain freedom, but no one can give you the right to self-government. This you must earn for yourself by long discipline.",
    "It is the person and not the sex which counts.",
]

images = [
    "https://assets.editorial.aetnd.com/uploads/2009/11/eleanor-roosevelt_gettyimages-507047802.jpg?width=768",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Eleanor-Franklin-Roosevelt-August-1932.jpg/220px-Eleanor-Franklin-Roosevelt-August-1932.jpg",
    "https://www.nps.gov/common/uploads/people/nri/20200325/people/BADABDD6-EC18-1B21-29DC983FCC47C1AA/BADABDD6-EC18-1B21-29DC983FCC47C1AA.jpg",
]

def home_page(request):
    '''Respond to the URL '', delegate work template.'''

    template_name = 'quotes/home.html'
    # a dict of context variables (key-value pairs) for /
    context = {
        'quote' : quotes[random.randint(0,2)],
        'image' : images[random.randint(0,2)],
    }

    return render(request, template_name, context)

def quote(request):
    '''Respond to the URL 'quote', delegate work template.'''

    template_name = 'quotes/home.html'
    # a dict of context variables (key-value pairs) for /quote
    context = {
        'quote' : quotes[random.randint(0,2)],
        'image' : images[random.randint(0,2)],
    }

    return render(request, template_name, context)

def about(request):
    '''Respond to the URL 'about', delegate work template.'''

    template_name = 'quotes/about.html'
     # a dict of context variables (key-value pairs) for /about
    return render(request, template_name)

def show_all(request):
    '''Respond to the URL 'show_all', delegate work template.'''

    template_name = 'quotes/show_all.html'
     # a dict of context variables (key-value pairs) for /show_all

    context = {
        'quotes' : quotes,
        'images' : images,
    }

    return render(request, template_name, context)