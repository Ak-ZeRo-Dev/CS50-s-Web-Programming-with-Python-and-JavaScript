from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name='watchers')
    bids = models.ManyToManyField('Listing', through='Bid', related_name='bidders')
    comments = models.ManyToManyField('Listing', through='Comment', related_name='commenters')


class Category(models.Model):
    category_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.category_name


class Listing(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=1000)
    price = models.FloatField()
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="listings_owner")
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, related_name="listings_category")
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="won_listings")
    
    def __str__(self):
        return self.title
    
    def current_highest_bid(self):
        highest_bid = self.bids.order_by('-amount').first()
        if highest_bid:
            return highest_bid.amount
        return self.price
    
    def get_winner(self):
        highest_bid = self.bids.order_by('-amount').first()
        if highest_bid:
            return highest_bid.user
        return self.user
    
        


class Bid(models.Model):
    listing = models.ForeignKey(Listing, blank=True, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='user_bids')
    amount = models.FloatField()
    
    def __str__(self):
        return f"Bid of {self.amount} by {self.user.username} on {self.listing.title}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, blank=True, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='user_comments')
    content = models.CharField(max_length=500)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"#{self.id}: {self.user.username} added a comment on {self.listing.title}"
