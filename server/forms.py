from django import forms
from django.contrib.auth.models import User
from models import List, Item


class ListForm(forms.ModelForm):
    class Meta:
        model = List


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item


class UserForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=30, min_length=6, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=30, min_length=4, required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'%s already exists' % username)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(u'User with %s email already exists' % email)
        