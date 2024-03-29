import traceback
from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from ..models import User, AuctionListing, Bid, WatchlistItem


@login_required()
def new_bid(request, listing_title):
    if request.method == "POST":
        amount = Decimal(request.POST["amount"])
        amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        listing = AuctionListing.objects.get(title=listing_title)

        highest_bid = Bid.objects.filter(listing=listing)
        highest_bid = highest_bid.order_by('-amount').first()
        print(highest_bid)

        print(amount)
        # validate price of new bid:
        if amount <= highest_bid.amount:
            return render(request, f"auctions/listing.html", {
                "listing": listing,
                "bid_message": "New bid must be greater than current bid."
            })

        try:
            new_bid = Bid(user=request.user, listing=listing, amount=amount)
            new_bid.save()
        except IntegrityError as e:
            traceback.print_exc()
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bid_message": "An error occurred. Please try again."
            })

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid_message": "Bid submitted."
        })
    else:
        return render(request, f"auctions/listing.html")

@login_required()
def new_comment(request, listing_title):
    pass

@login_required()
def remove_listing(request, listing_title):
    if request.method == "POST":
        listing = AuctionListing.objects.get(title=listing_title)
        if listing.user == request.user:
            try:
                listing.delete()
                return HttpResponseRedirect(reverse("index"))
            except IntegrityError as e:
                traceback.print_exc()
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "message": "An error occurred. Please try again."
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "You must be the owner of this listing to delete the listing."
            })
    else:
        return HttpResponseRedirect(reverse("index"))
    pass


@login_required()
def add_to_watchlist(request, listing_title):
    if request.method == "POST":
        listing = AuctionListing.objects.get(title=listing_title)
        try:
            new_watchlist_item, created = WatchlistItem.objects.get_or_create(user=request.user, listing=listing)
            if created:
                message = "Added to watchlist."
            else:
                message = "This item is already in your watchlist."
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "add_to_watchlist_message": message
            })
            pass
        except IntegrityError as e:
            traceback.print_exc()
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "add_to_watchlist_message": "An error occurred. Please try again."
            })
    else:
        return render(request, "auctions/listing.html", {
            "add_to_watchlist_message": "An error occurred. Please try again."
        })
    pass


def watchlist(request):
    listings_with_bids = []
    watchlist_items = WatchlistItem.objects.filter(user=request.user)
    for item in watchlist_items:
        listing = item.listing
        print(listing)
        highest_bid = Bid.objects.filter(listing=listing)
        print(highest_bid)
        highest_bid = highest_bid.order_by('-amount').first()
        listings_with_bids.append((listing, highest_bid))
    return render(request, "auctions/watchlist.html", {
        "listings": listings_with_bids
    })
