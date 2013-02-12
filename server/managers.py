
from django.db import models
from django.template.defaultfilters import slugify


class ListManager(models.Manager):
    def create_list(self, name, description, user):
        slug = slugify(name)
        return super(ListManager, self).create(name=name, slug = slug, description=description, user=user)
