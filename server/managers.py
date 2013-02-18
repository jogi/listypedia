
from django.db import models
from django.template.defaultfilters import slugify


class ListManager(models.Manager):
    def create_list(self, name, description, user):
        slug = slugify(name)
        return super(ListManager, self).create(name=name, slug=slug, description=description, user=user)

    def get_lists_by_user(self, user, collaborator=True):
        return None


class ItemManager(models.Manager):
    def create_item(self):
        return super(ItemManager, self).create()


class FollowerManager(models.Manager):
    def create_follower(self, user, list):
        return super(FollowerManager, self).create(user=user, list=list)
