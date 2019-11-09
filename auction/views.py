from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Auction_list
from . import forms
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q




def index(request):
    data=Auction_list.objects.all()
    return render(request, './auction/home.html', {"head": "All Auctions", "data": data})


def search(request):
    if request.method == 'GET':
        query = request.GET.get('term')
        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(title__iexact=query)
            results = Auction_list.objects.filter(lookups)
            context = {'results': results, 'submitbutton': submitbutton}
            return render(request, './auction/search.html', context)
        else:
            return render(request, './auction/search.html')
    else:
        return render(request, './auction/search.html')



def user_page(request):
    data=Auction_list.objects.all()
    return render(request, './auction/my_page.html', {"head": "My Auction ", "data": data})

class CreateAuction(View):
    form_class = forms.create_auction()
    def get(self, request):
        form = self.form_class
        return render(request, './auction/create.html', {"head": "Create Auction", "form": form})

    def post(self, request):
        form = forms.create_auction(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            desc = form.cleaned_data["description"]
            price = form.cleaned_data["min_price"]
            deadline = form.cleaned_data["deadline"]
            list = Auction_list(title=title, description=desc, min_price=price, deadline=deadline)
            list.save()
            request.user.user_auction.add(list)

            mail_subject = 'Auction created'
            message = 'Your auction is created'
            sender = settings.EMAIL_HOST_USER
            to_email = [request.user.email, ]
            send_mail(
                mail_subject,
                message,
                sender,
                to_email,
                fail_silently=False,
            )

            messages.add_message(request, messages.INFO, 'Auction Created!')
            return redirect("/auction")

        return render(request, './auction/create.html', {"head": "Create Auction", "form": form})

class EditAuction(View):
    def get(self, request, id):
        post= get_object_or_404(Auction_list, id=id)
        form = forms.create_auction(instance=post)
        return render(request, './auction/edit.html', {"head": "Edit Auction", "form": form})

    def post(self, request, id):
        post = get_object_or_404(Auction_list, id = id)
        form = forms.create_auction(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.INFO,'Updated!')
            return redirect("/auction")

        return render(request, './auction/edit.html', {"head": "Edit Auction", "form": form})



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


