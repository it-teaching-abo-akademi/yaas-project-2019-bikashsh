from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Auction_list, Language, Bid
from . import forms
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.utils import translation, timezone
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
import decimal

from django.contrib.auth.models import User


def index(request):

    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]

    data = Bid.objects.all()
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
            bid = 0.1
            bid_data = Bid(bidprice=bid, itemid_id=list.id, user_id=request.user.id)
            bid_data.save()

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
        post = get_object_or_404(Auction_list, id=id)
        form = forms.create_auction(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.INFO,'Updated!')
            return redirect("/auction")

        return render(request, './auction/edit.html', {"head": "Edit Auction", "form": form})


@login_required(login_url='/signin/')
def bid(request, item_id):
    auction = get_object_or_404(Auction_list, id=item_id)
    if not auction.state == "A":
        messages.add_message(request, messages.ERROR, 'Sorry, The bid is not active')
        return HttpResponseRedirect('/auction')
    if request.user.username == auction.user.username:
        messages.add_message(request, messages.ERROR, 'You cannot bid in your own auction')
        return HttpResponseRedirect('/auction')
    else:
        if not request.method == 'POST':
            form = forms.Bidform(request.POST)

            return render(request, "./auction/bid.html", {'head': auction.title, 'form': form})

            # print 'is not seller'
        form = forms.Bidform(request.POST)
        new_bid_raw = request.POST['bidprice']

        try:
            new_bid_dec = decimal.Decimal(new_bid_raw)
        except InvalidOperation:
            return render(request, "./auction/bid.html", {'head': auction.title, 'form': form})

        new_bid = Bid.objects.get(id=item_id)
        bid_price = new_bid_dec
        highest_bid = new_bid.bidprice
        if bid_price > highest_bid:

            new_bid.bidprice = bid_price
            new_bid.user = request.user
            messages.add_message(request, messages.INFO, 'Bid successfull')
            new_bid.save()
            #Email Bidder
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email,]
            send_mail('Bidding Placed','Thank you for placing bid. We will notify if you win.',email_from,recipient_list,fail_silently=False,)
            ##Email Seller
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [auction.user.email,]
            send_mail('Bidding Placed in your item','A bid has been placed in your item..',email_from,recipient_list,fail_silently=False,)

            return HttpResponseRedirect('/auction')
        else:
            messages.add_message(request, messages.ERROR, 'Bid is not higher than current bid')
            return render(request, "./auction/bid.html", {'head': auction.id, 'form': form})


def ban(request, ban_id):
    auction = get_object_or_404(Auction_list, id=ban_id)
    if request.method == 'POST':
        print("Inside post")

        form = forms.Banform(request.POST)
        new_state = request.POST['state']
        state = Auction_list.objects.get(id=ban_id)
        state.state = new_state
        messages.add_message(request, messages.INFO, 'Auction banned')
        state.save()
        #Email Bidder
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email,]
        send_mail('Bidding Placed','Thank you for placing bid. We will notify if you win.',email_from,recipient_list,fail_silently=False,)
        ##Email Seller
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [auction.user.email,]
        send_mail('Bidding Placed in your item','A bid has been placed in your item..',email_from,recipient_list,fail_silently=False,)

        return HttpResponseRedirect('/auction')
    else:
        form = forms.Banform(request.POST)
        return render(request, "./auction/ban.html", {'head': auction.id, 'form': form})


def resolve(request):
    if request.method == 'GET':
        auction = Auction_list.objects.filter(state="A")
        current_time = timezone.now()
        print("Inside time" + str(current_time))
        resolved_auctions = []

        for item in auction:

            if item.deadline <= current_time:
                bid = Bid.objects.get(itemid=item.id)
                print(bid.user.email)
                item.state = "R"
                item.save()
                messages.add_message(request, messages.INFO, 'Auction Resolved')
                if(bid.user.email==item.user.email):
                  email_from = settings.EMAIL_HOST_USER
                  recipient_list = [item.user.email,]
                  send_mail('No Bid','No bidding was placed in your item',email_from,recipient_list,fail_silently=False,)
                else:
                  ##Email Bidder
                  email_from = settings.EMAIL_HOST_USER
                  recipient_list = [bid.user.email,]
                  send_mail('Congratulations','Congratulations you have won the bid. Please pay and enjoy.',email_from,recipient_list,fail_silently=False,)
                #Email Seller
                  email_from = settings.EMAIL_HOST_USER
                  recipient_list = [auction.user.email,]
                  send_mail('Item auctioned',('Your item has been won by '+str(bid.user.username)),email_from,recipient_list,fail_silently=False,)

                resolved_auctions.append(item.title)
        content = {"resolved_auctions": resolved_auctions}
        return JsonResponse(content)
    else:
        messages.add_message(request, messages.INFO, 'Auction not resolved')
    return HttpResponseRedirect("/auction")

def changeLanguage(request, lang_code):

    language_pref = lang_code
    translation.activate(lang_code)
    request.session[translation.LANGUAGE_SESSION_KEY] = language_pref
    if lang_code == 'sv':
        messages.add_message(request, messages.SUCCESS, _("Du ar pa svenska sidan!"))
    elif lang_code == 'en':
        messages.add_message(request, messages.SUCCESS, _("You are in English page!"))

    if request.user.is_authenticated:
        language_preference = Language.objects.filter(user=request.user)
        if language_preference is None:
            language_preference.user_language = language_pref
    # auctions = Auction_list.objects.filter(state="Active")
    return render(request, './auction/home.html', {"head": "Active Auctions"})

def changeCurrency(request, currency_code):
    pass