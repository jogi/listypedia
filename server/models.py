from django.db import models
from django.contrib.auth.models import User

from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField

from server import managers


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class List(BaseModel):
    name = models.CharField(max_length=300, null=False)
    slug = models.SlugField(max_length=300, null=False, unique=True, db_index=True)
    description = models.TextField()
    user = models.ForeignKey(User, null=False)
    privacy_level = models.IntegerField(default=1)
    search_index = VectorField()

    objects = managers.ListManager()
    sobjects = SearchManager(
        fields=('name', 'description'),
        config='pg_catalog.english',  # this is default
        search_field='search_index',  # this is default
        auto_update_search_field=True
    )


class Item(BaseModel):
    name = models.CharField(max_length=300)
    description = models.TextField()
    url = models.CharField(max_length=300)
    user = models.ForeignKey(User, null=False)
    list = models.ForeignKey(List, null=False)
    search_index = VectorField()

    objects = managers.ItemManager()
    sobjects = SearchManager(
        fields=('name', 'description', 'url'),
        config='pg_catalog.english',  # this is default
        search_field='search_index',  # this is default
        auto_update_search_field=True
    )


class CollaborationInvitation(BaseModel):
    user = models.ForeignKey(User, null=False)
    list = models.ForeignKey(List, null=False)
    email = models.EmailField(null=False)
    code = models.CharField(max_length=50, null=False)


class Collaborator(BaseModel):
    user = models.ForeignKey(User, null=False)
    list = models.ForeignKey(List, null=False)


class Follower(BaseModel):
    user = models.ForeignKey(User, null=False)
    list = models.ForeignKey(List, null=False)
    objects = managers.FollowerManager()
