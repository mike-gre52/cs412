#file: restaurant/views.py

# Created by Mike Greene

# file for view functions corresponding to urls

from django.shortcuts import render

import time
import random

# Create your views here.
def main(request):
    '''Defines a view to handle the 'main' request.'''

    template_name = "restaurant/main.html"
    return render(request, template_name)

def order(request):
    '''Defines a view to handle the 'order' request.'''

    specials = [
        "spicy tomato sauce",
        "cheesy garlic bread",
        "Free french fries",
        "Free soda"
    ]

    context = {
        'special' : specials[random.randint(0,3)],
    }

    template_name = "restaurant/order.html"
    return render(request, template_name, context)

def submit(request):
    '''Process the order submission, and generate a result.'''

    template_name = "restaurant/confirmation.html"

    # read the form data into python variables:
    if request.POST:

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        special_instructions = request.POST.get("special_instructions", "")
        special = request.POST.get("special")
        order_items = request.POST.getlist("items")

        print("Special: ", special)

        items = {
            "item1": "Chicken Parmesan Sub $18",
            "item2": "Meatball Sub $15",
            "item3": "Fettuccine Alfredo $15",
            "item3.1": "Add Chicken $4",
            "item3.2": "Add Broccoli $2",
        }

        order = []

        for item in order_items:
            print(item)
            order.append(items[item]) 

        if special != "":
            order.append(special)

        prices = {
            "item1": 18,
            "item2": 15,
            "item3": 15,
            "item3.1": 4,
            "item3.2": 2,
        }


        price = 0
      

        for item in order_items:
            price += prices[item]

       
        current_time = time.time()
        future_time = current_time + random.randint(1800, 3200)
        order_time = time.ctime(future_time)
    

        print(order)

        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'special': special,
            'special_instructions': special_instructions,
            'price': price,
            'order': order,
            'order_time': order_time,
            
        }
    #delegate the response to the template, provide context variables
    return render(request, template_name, context=context)