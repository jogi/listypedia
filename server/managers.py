
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify


class ListManager(models.Manager):
    def create_list(self, name, description, user):
        slug = slugify(name)
        return super(ListManager, self).create(name=name, slug=slug, description=description, user=user)

    def get_lists_by_user(self, user, collaborator=True):
        query = Q(user=user)
        if collaborator:
            query = query | Q(collaborator=user)
        return super(ListManager, self).filter(query)

    def get_followed_lists_by_user(self, user):
        return super(ListManager, self).filter(follower=user)

    def get_collaborated_lists_by_user(self, user):
        return super(ListManager, self).filter(collaborator=user)


class ItemManager(models.Manager):
    def create_item(self):
        return super(ItemManager, self).create()


class FollowerManager(models.Manager):
    def create_follower(self, user, list):
        return super(FollowerManager, self).create(user=user, list=list)
