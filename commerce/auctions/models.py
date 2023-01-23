import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    
    def __str__(self):
        return f"{self.username}"
    
class Listing(models.Model):
    id= models.BigAutoField(primary_key=True)
    title= models.CharField(max_length=25)
    description= models.CharField(max_length=150)
    category= models.CharField(max_length=25)
    img = models.CharField(max_length=300)
    startBid = models.DecimalField(decimal_places=2,max_digits=8)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_listing")
    sold = models.BooleanField(default=False)
    biggest_bid = models.DecimalField(decimal_places=2,max_digits=8,default=0)
    
    def __str__(self):
        return f"{self.title}: {self.owner}"
    
class WatchList(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    watchlist = models.ManyToManyField(Listing,blank=True, related_name="item_watchlist")
    
    def __str__(self):
        return f"{self.user}: {self.watchlist}"
    
class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    price = models.DecimalField(decimal_places=2,max_digits=8)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user", default="1")
    
    def __str__(self):
        return f"{self.user}: ${self.price}"
    
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=100)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user", default="1")
    
    def __str__(self):
        return f"{self.user}: {self.text}"
    
