from django.contrib.auth.models import AbstractUser
from django.db import models

# Each time you change a line here, 
# Remember to run `python manage.py makemigrations`
# Then, run `python manage.py migrate`

class User(AbstractUser):
    # Watchlist
    # List of active bids
    pass

class AuctionListing(models.Model):
    username = models.CharField(max_length=255)
    post_date = models.DateTimeField() 
    end_date = models.DateTimeField()
    listing_name = models.TextField()
    description = models.TextField()
    photo = models.ImageField(upload_to='uploads/%Y/%m/%d/')

class Bid(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=9)

class Comment(models.Model):
    pass


