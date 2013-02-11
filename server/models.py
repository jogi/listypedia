from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
        
class List(BaseModel):
    name = models.CharField(max_length=300, null=False)
    description = models.TextField()
    user = models.ForeignKey(User, null=False)
    privacy_level = models.IntegerField(default=1)
    
class Item(BaseModel):
    name = models.CharField(max_length=300)
    description = models.TextField()
    url = models.CharField(max_length=300)
    user = models.ForeignKey(User, null=False)
    list = models.ForeignKey(List, null=False)
    
class CollaborationInvitation(BaseModel):
    user = models.ForeignKey(User, null=False)
    list = models.ForeignKey(List, null=False)
    email = models.EmailField(null=False)
    
class Collaborator(BaseModel):
    user = models.ForeignKey(User, null=False)
    list = models.ForeignKey(List, null=False)
    
class Follower(BaseModel):
    user = models.ForeignKey(User, null=False)
    list = models.ForeignKey(List, null=False)
    
    