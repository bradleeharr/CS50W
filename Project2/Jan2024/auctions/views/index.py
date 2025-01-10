from django.shortcuts import render

from ..models import AuctionListing, Bid


def index(request):
    listings_with_bids = []
    listings = AuctionListing.objects.all()
    for listing in listings:
        highest_bid = Bid.objects.filter(listing=listing)
        highest_bid = highest_bid.order_by('-amount').first()
        listings_with_bids.append((listing, highest_bid))
    return render(request, "auctions/index.html", {
        "listings": listings_with_bids
    })
