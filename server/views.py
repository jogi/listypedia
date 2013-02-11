import logging
import emailutil

from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib import auth
from forms import ListForm, ItemForm, UserForm, LoginForm
from django.template.defaultfilters import slugify
from server.models import List, Item

# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    return render_to_response('index.html')


def home(request):
    your_lists = List.objects.filter(user__id=request.user.id)
    followed_lists = List.objects.filter(user__id=request.user.id)

    return render_to_response('home.html', {'your_lists': your_lists, 'followed_lists': followed_lists})


def create_list(request):
    if request.method == 'GET':
        logger.info("creating new list form")
        form = ListForm()
        return render(request, 'create_list.html', {
            'form': form,
        })
    elif request.method == 'POST':
        logger.info("saving a new list")
        form = ListForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            slug = slugify(name)
            description = form.cleaned_data['description']
            print request.user.id
            user = request.user
            list = List.objects.create(name=name, slug = slug, description=description, user=user)
            if list:
                return HttpResponseRedirect('/list/%s' % list.pk)
        else:
            return render(request, 'create_list.html', {'form': form})
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
            user = auth.authenticate(username=user.username, password=user.password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect('/home/')  # Redirect after POST
        else:
            return render(request, 'signup.html', {'form': form})

    else:
        logger.info("invalid operation")


def view_list(request, list):
    try:
        list = List.objects.get(slug=list)
        items = Item.objects.filter(list=list)
    except List.DoesNotExist:
        raise Http404
    return render_to_response('view_list.html', {'list': list, 'items': items})


def add_item(request, list):
    logger.info("In add_item")
    list = List.objects.get(pk=list)
    if request.method == 'GET':
        form = ItemForm()
        return render(request, 'add_item.html', {'form': form, 'list': list})
    elif request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            url = form.cleaned_data['url']
            user = request.user
            item = Item.objects.create(name=name, description=description, url=url, list=list, user=user)
            if item:
                return HttpResponseRedirect('/list/%s' % list.id)
        else:
            return render(request, 'add_item.html', {'form': form})


def add_collabarator(request):
    logger.info("In add_collabarator")


def add_follower(request):
    logger.info("In follow_list")


def login(request):
    messages = []
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/home/')
        else:
            return render_to_response('login.html')
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.get(email=email)
            if user:
                user = auth.authenticate(username=user.username, password=password)
                if user != None:
                    auth.login(request, user)
                    return HttpResponseRedirect('/home/')
                else:
                    messages.append("Email or password incorrect")
                    return render_to_response('login.html', {'form': form, 'messages': messages})
            else:
                messages.append("Email or password incorrect")
                return render_to_response('login.html', {'form': form, 'messages': messages})
        else:
            return render_to_response('login.html', {'form':form})

        
def logout_user(request):
    auth.logout(request)
    return redirect("/")
