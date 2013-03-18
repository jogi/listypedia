from urlparse import urlparse

from django.db import models
from django.contrib.auth.models import User

from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField

from autoslug import AutoSlugField

from server import managers


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class List(BaseModel):
    name = models.CharField(max_length=300, null=False)
    slug = AutoSlugField(populate_from='name', null=False, unique=True, db_index=True)
    description = models.TextField()
    user = models.ForeignKey(User, null=False)
    privacy_level = models.IntegerField(default=1)
    featured = models.BooleanField(default=False)
    search_index = VectorField()

    objects = managers.ListManager()
    sobjects = SearchManager(
        fields=('name', 'description'),
        config='pg_catalog.english',  # this is default
        search_field='search_index',  # this is default
        auto_update_search_field=True
    )

    @property
    def url(self):
        return 'list/%s' % self.slug

    @property
    def followers(self):
        return self.follower_set.all()

    @property
    def items(self):
        return self.item_set.all()

    @property
    def featured_items(self):
        return self.item_set.filter(active=True)[:3]

    @property
    def collaborators(self):
        return self.collaborator_set.all()


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

    @property
    def url_domain(self):
        if self.url:
            return urlparse(self.url).hostname
        else:
            return 'listypedia.com'


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
