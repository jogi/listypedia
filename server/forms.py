from django.forms import ModelForm
from django.contrib.auth.models import User
from models import List,Item

class ListForm(ModelForm):
    class Meta:
        model = List
        
class ItemForm(ModelForm):
    class Meta:
        model = Item
        
class UserForm(ModelForm):
    class Meta:
        model = User
        