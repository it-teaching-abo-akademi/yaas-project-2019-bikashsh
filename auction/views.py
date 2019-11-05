from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Auction_list
from . import forms
from django.contrib import messages


def index(request):
    data=Auction_list.objects.all()
    return render(request, './auction/home.html', {"head": "Auctions", "data": data})


def search(request):
    pass


class CreateAuction(View):
    form_class = forms.create_auction()
    def get(self, request):
        form = self.form_class
        return render(request, './auction/create.html', {"head": "Create Auction", "form": form})

    def post(self, request):
        form = forms.create_auction(data=request.POST)
        if form.is_valid:
            form.save()
            messages.add_message(request,messages.INFO, 'Auction Created!')
            return redirect("/auction")
        else:
            print("hello")
        return render(request, './auction/create.html', {"head": "Create Auction", "form": form})

class EditAuction(View):
    pass


def bid(request, item_id):
    pass


def ban(request, item_id):
    pass


def resolve(request):
    pass


def changeLanguage(request, lang_code):
    pass


def changeCurrency(request, currency_code):
    pass


