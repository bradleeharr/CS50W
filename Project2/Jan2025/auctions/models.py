from django.contrib.auth.models import AbstractUser
from django.db import models

# Each time you change a line here, 
# Remember to run `python manage.py makemigrations`
# Then, run `python manage.py migrate`

class User(AbstractUser):
    # Watchlist
    # List of active bids
    pass

class AuctionListing():
    # title
    # description
    # current price
    # photo (if exists)
    pass

class Bid():
    pass

class Comment():
    pass


