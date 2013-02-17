import logging
import urllib
import bs4
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from forms import ListForm, ItemForm, UserForm, FollowerForm, CollaborationInvitationForm
from server.models import List, Item, Follower, Collaborator, CollaborationInvitation
from server import emailutil
import uuid
from django.utils import simplejson
# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


@login_required
def home(request):
    your_lists = List.objects.filter(user=request.user)
    followed_lists = List.objects.filter(user=request.user)

    return render(request, 'home.html', {
        'your_lists': your_lists,
        'followed_lists': followed_lists
    })


@login_required
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
                follower = Follower.objects.create_follower(user=user, list=list)
                if follower:
                    #emailutil.send_follow_confirmation_email(user, list)
                    return HttpResponseRedirect('/list/%s' % list.slug)
                else:
                    return HttpResponse(status=500)
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
    followed = False
    creator = False
    collaborator = False
    try:
        list = List.objects.get(slug=slug)
        items = Item.objects.filter(list=list)
        if request.user.is_authenticated():
            try:
                follower = Follower.objects.filter(user=request.user, list=list,active=True)
                if follower:
                    followed = True
            except Follower.DoesNotExist:
                followed = False

            try:
                collaborator_user = Collaborator.objects.get(user=request.user)
                if collaborator_user:
                    collaborator = True
            except Collaborator.DoesNotExist:
                collaborator = False

            if request.user.id == list.user.id:
                creator = True
            if creator or collaborator_user:
                collaborator = True
    except List.DoesNotExist:
        raise Http404
    return render(request, 'view_list.html', {
        'list': list,
        'items': items,
        'followed': followed,
        'creator': creator,
        'collaborator': collaborator,
    })


@login_required
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
                followers = Follower.objects.filter(list=list,active=True)
                emailutil.send_item_add_notification_email(user, list, item, followers)
                return HttpResponseRedirect('/list/%s' % list.slug)
        else:
            return render(request, 'add_item.html', {
                'form': form,
                'list': list
            })


@login_required
def invite_collaborator(request, slug):
    logger.info("In invite_collabarator")
    list = List.objects.get(slug=slug)
    if request.method == 'GET':
        current_invitees = CollaborationInvitation.objects.filter(list=list)
        return render(request, 'collaboration_invitation.html', {
            'list': list,
            'current_invitees': current_invitees,
        })
    elif request.method == 'POST':
        form = CollaborationInvitationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = request.user
            collabarator_invitation = CollaborationInvitation.objects.create(user=user, list=list, email=email, code=uuid.uuid1())
            if collabarator_invitation:
                emailutil.send_collabaration_invitation_email(user, list, collabarator_invitation)
                return HttpResponseRedirect('/list/%s/invite' % list.slug)
        else:
            current_collaborators = CollaborationInvitation.objects.filter(list=list)
            return render(request, 'collaboration_invitation.html', {
                'list': list,
                'current_collaborators': current_collaborators,
                'form': form,
            })


@login_required
def accept_invitation(request):
    logger.info("In accept_invitation")
    print "in accept"
    try:
        code = request.GET["c"]
        invitation = CollaborationInvitation.objects.get(code=code)
        if invitation:
            collaborator = Collaborator.objects.create(user=request.user, list=invitation.list)
            if collaborator:
                return HttpResponseRedirect('/list/%s/item/add/' % invitation.list.slug)
    except CollaborationInvitation.DoesNotExist:
        raise Http404


@login_required
def add_follower(request):
    logger.info("In follow_list")
    form = FollowerForm(request.POST)
    if form.is_valid():
        list_id = form.cleaned_data['list_id']
        list = List.objects.get(pk=list_id)
        user = request.user
        try:
            follower = Follower.objects.get(user=user, list=list)
            if follower:
                follower.active = True
                follower.save()
            else:
                follower = Follower.objects.create_follower(user=user, list=list)
        except Follower.DoesNotExist:
                follower = Follower.objects.create_follower(user=user, list=list)
        if follower:
            #emailutil.send_follow_confirmation_email(user, list)
            return render(request, 'follow_confirmation.html', {
                'list': list,
            })
        else:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)
    
@login_required
def remove_follower(request):
    logger.info("In follow_list")
    form = FollowerForm(request.POST)
    if form.is_valid():
        list_id = form.cleaned_data['list_id']
        list = List.objects.get(pk=list_id)
        user = request.user
        follower = Follower.objects.get(user=user, list=list)
        follower.active = False
        follower.save()
        if follower:
            return HttpResponseRedirect('/list/%s' % list.slug)
        else:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)


def search(request):
    print repr(request.POST)
    query = request.POST['q']
    lists = List.sobjects.search(query)
    return render(request, 'search.html', {
        'lists': lists,
        'query': query
    })
    
def page_info(request):
    url = request.GET["u"]
    page_info = {}
    page_info["url"] = url
    try:
        soup = bs4.BeautifulSoup(urllib.urlopen(url),"lxml")
        page_info["title"] = soup.title.string
    except:
        page_info["title"] = ""
    return HttpResponse(simplejson.dumps(page_info), mimetype='application/json')
