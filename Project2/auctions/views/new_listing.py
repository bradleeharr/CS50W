import traceback

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auctions.models import AuctionListing, Bid


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

