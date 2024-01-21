from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Now


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    title = models.TextField(default="Title")
    content = models.TextField(default="Content")
    #start_date = models.DateTimeField(default=Now())
    #end_date = models.DateTimeField(default=Now())
    pass


class Bid(models.Model):
    pass


class Comment(models.Model):
    pass

