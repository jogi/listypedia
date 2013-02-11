from django.shortcuts  import render_to_response, redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from forms import ListForm,UserForm
import sys, traceback
import logging
import emailutil

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    return render_to_response('index.html')

def new_list(request):
    logger.info("In create_list")

    
def create_list(request):
    if request.method == 'GET':
        logger.info("creating new list form")
        form = ListForm()
        return render(request, 'create_list.html', {
            'form': form,
        })
    elif request.method == 'POST':
        logger.info("saving a new list")
    else:
        logger.info("invalid operation")
        
def signup(request):
    if request.method == 'GET':
        logger.info("creating new user form")
        form = UserForm()
        return render(request, 'signup.html', {
            'form': form,
        })
    elif request.method == 'POST':
        logger.info("saving a new list")
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            emailutil.send_welcome_email(user)
            return HttpResponseRedirect('/') # Redirect after POST
        else:
            return render(request, 'signup.html', {
                'form': form,
            })  

    else:
        logger.info("invalid operation")
    
def view_list(request,pk):
    logger.info("In view_list")
    
def add_item(request):
    logger.info("In add_item")
    
def add_collabarator(request):
    logger.info("In add_collabarator")
    
def add_follower(request):
    logger.info("In follow_list")
    

    