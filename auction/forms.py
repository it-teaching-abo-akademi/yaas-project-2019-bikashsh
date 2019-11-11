from django import forms
from .models import Auction_list
from django.utils import timezone


class create_auction(forms.ModelForm):


    class Meta:
        model = Auction_list
        fields =["title", "description", "min_price", "deadline"]


    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        min_deadline = timezone.now() + timezone.timedelta(hours=72)
        if deadline <= min_deadline:
            raise forms.ValidationError("The deadline should be at least 72 hours from the time it was created.")
        return deadline


class EditAuction(forms.ModelForm):
    class Meta:
        model =Auction_list
        fields = ["title", "description", "min_price", "deadline"]


class Bidform(forms.Form):
    bidprice = forms.DecimalField(max_digits=10, decimal_places=2)


class Banform(forms.ModelForm):
    class Meta:
        model = Auction_list
        fields = ["state"]