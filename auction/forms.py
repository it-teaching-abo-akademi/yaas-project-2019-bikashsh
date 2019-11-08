from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Auction_list
from django.utils import timezone


class create_auction(forms.ModelForm):

    class Meta:
        model = Auction_list
        fields =["title", "description", "min_price", "deadline"]

