import datetime

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User
from .models import AuctionListing

def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


class NewListingForm(forms.Form):
    listing_name = forms.CharField(label="Listing Name")
    description = forms.CharField(widget=forms.Textarea)
    end_date = forms.DateTimeField(initial=datetime.date.today() + datetime.timedelta(days=1) )
    bid = forms.DecimalField(label="Starting Bid", initial=1.00)
    photo = forms.ImageField(required=False)


def new_listing(request):
    if request.method == "POST":
        username = str(request.user)
        post_date = datetime.datetime.now()
        listing_name = request.POST["listing_name"]
        end_date = request.POST["end_date"] 
        description = request.POST["description"]
        # photo = models.ImageField(upload_to='uploads/%Y/%m/%d/')

        try:
            auction_listing = AuctionListing.objects.create(
                username = username,
                post_date = post_date,
                end_date = end_date,
                listing_name = listing_name,
                description = description,
            )
            auction_listing.save()
        except IntegrityError as e:
            return render(request, "auctions/new_listing.html", {
                "form": NewListingForm(),
                "message": f"Integrity Error {e}."
            })

        return render(request, "auctions/new_listing.html", {
            "form": NewListingForm(),
            "message": "POST Received on Server."
        })
    else:
        return render(request, "auctions/new_listing.html", {
            "form": NewListingForm()
        })