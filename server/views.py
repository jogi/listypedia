import logging
import emailutil

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib import auth
from forms import ListForm, ItemForm, UserForm, LoginForm
from server.models import List, Item

# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


def home(request):
    your_lists = List.objects.filter(user=request.user)
    followed_lists = List.objects.filter(user=request.user)

    return render(request, 'home.html', {
        'your_lists': your_lists,
        'followed_lists': followed_lists
    })


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
            description = form.cleaned_data['description']
            user = request.user
            list = List.objects.create_list(name=name, description=description, user=user)
            if list:
                return HttpResponseRedirect('/list/%s' % list.slug)
        else:
            return render(request, 'create_list.html', {
                'form': form
            })
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
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return HttpResponseRedirect('/home/')  # Redirect after POST
        else:
            return render(request, 'signup.html', {
                'form': form
            })

    else:
        logger.info("invalid operation")


def view_list(request, slug):
    try:
        list = List.objects.get(slug=slug)
        items = Item.objects.filter(list=list)
    except List.DoesNotExist:
        raise Http404
    return render(request, 'view_list.html', {
        'list': list,
        'items': items
    })


def add_item(request, slug):
    logger.info("In add_item")
    list = List.objects.get(slug=slug)
    if request.method == 'GET':
        form = ItemForm()
        return render(request, 'add_item.html', {
            'form': form,
            'list': list
        })
    elif request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            url = form.cleaned_data['url']
            user = request.user
            item = Item.objects.create(name=name, description=description, url=url, list=list, user=user)
            if item:
                return HttpResponseRedirect('/list/%s' % list.slug)
        else:
            return render(request, 'add_item.html', {
                'form': form
            })


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
            return render(request, 'login.html')
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
                    return render(request, 'login.html', {
                        'form': form,
                        'messages': messages
                    })
            else:
                messages.append("Email or password incorrect")
                return render(request, 'login.html', {
                    'form': form,
                    'messages': messages
                })
        else:
            return render(request, 'login.html', {
                'form': form
            })


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def search(request):
    print repr(request.POST)
    query = request.POST['q']
    lists = List.sobjects.search(query)
    return render(request, 'search.html', {
        'lists': lists,
        'query': query
    })
