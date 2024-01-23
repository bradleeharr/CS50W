import traceback

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime

from .models import User, AuctionListing, Bid


def index(request):
    listings_with_bids = []
    listings = AuctionListing.objects.all()
    for listing in listings:
        highest_bid = Bid.objects.filter(listing=listing)
        print(highest_bid)
        highest_bid = highest_bid.order_by('-amount').first()
        listings_with_bids.append((listing, highest_bid))
    return render(request, "auctions/index.html", {
        "listings": listings_with_bids
    })




@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def listing(request, listing_title):
    listing = AuctionListing.objects.filter(title=listing_title)
    return render(request, f"auctions/listing.html", {
        "listing": listing.get()
    })


@login_required
def new_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        amount = request.POST["amount"]
        description = request.POST["description"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        image = request.FILES.get('image')

        # validate end date and start date
        if end_date <= start_date:
            return render(request, "auctions/new_listing.html", {
                "message": "End date must be after the start date."
            })

        try:
            listing = AuctionListing(user=request.user, title=title, description=description,
                                     start_date=start_date, end_date=end_date, image=image)
            listing.save()
            starting_bid = Bid(user=request.user, listing=listing, amount=amount)
            starting_bid.save()
        except IntegrityError as e:
            traceback.print_exc()
            return render(request, "auctions/new_listing.html", {
                "message": "An error occurred: " + str(e)
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, f"auctions/new_listing.html")


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
        except ValueError:
            return render(request, "auctions/register.html", {
                "message": "Make sure all fields are filled out correctly."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


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
