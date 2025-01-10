from django.shortcuts import render

from auctions.models import AuctionListing


def listing(request, listing_title):
    listing = AuctionListing.objects.filter(title=listing_title)
    return render(request, f"auctions/listing.html", {
        "listing": listing.get()
    })
