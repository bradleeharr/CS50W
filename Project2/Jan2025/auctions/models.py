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
    post_date = models.DateField() 
    end_date = models.DateField()
    title = models.TextField()
    description = models.TextField()
    photo = models.ImageField(upload_to='uploads/%Y/%m/%d/')

class Bid():
    price = models.DecimalField()
    pass

class Comment():
    pass


