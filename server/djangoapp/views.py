from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf,\
    get_dealer_by_state_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    context["contentBody"]="about"
    return render(request, 'djangoapp/index.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    context["contentBody"]="contact"
    return render(request, 'djangoapp/index.html', context)
# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('djangoapp:index')

    context = {}
    context["contentBody"]="home"
    return render(request, 'djangoapp/index.html',context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        context["contentBody"]="register"
        return render(request, 'djangoapp/index.html', context)
    elif request.method == "POST":
        user_exists = False
        username = request.POST['username']
        try:
            User.objects.get(username=username)
            user_exists = True
        except:
            logger.debug("{} is available for use".format(username))

        if not user_exists:
            password = request.POST['password']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user= User.objects.create_user(username=username, password=password, email=email,first_name=first_name, last_name=last_name)   
            return redirect("djangoapp:index")

    context["contentBody"]="home"
    return render(request, 'djangoapp/index.html', context)        


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        # Get dealers from the URL
        dealerships = get_dealers_from_cf()
        # Return a list of dealer short name
        context["contentBody"] = "home"
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(dealer_id)
        dealer = get_dealer_by_id_from_cf(dealer_id)
        # Return a list of dealer short name
        context["contentBody"] = "dealer"
        context["dealer"] = dealer
        context["reviews"] = reviews
        return render(request, 'djangoapp/index.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

