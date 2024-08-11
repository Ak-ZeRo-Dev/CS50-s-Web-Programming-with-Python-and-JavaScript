from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Category, Bid, Comment
from django.contrib.auth.models import AnonymousUser

def index(req):
    listings = Listing.objects.filter(is_active=True)
    return render(req, "auctions/index.html", {
        "listings": listings,
        "type": "index",
    })


def login_view(req):
    if req.method == "POST":

        # Attempt to sign user in
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(req, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(req, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(req, "auctions/login.html")


def logout_view(req):
    logout(req)
    return HttpResponseRedirect(reverse("index"))


def register(req):
    if req.method == "POST":
        username = req.POST["username"]
        email = req.POST["email"]

        # Ensure password matches confirmation
        password = req.POST["password"]
        confirmation = req.POST["confirmation"]
        if password != confirmation:
            return render(req, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(req, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(req, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(req, "auctions/register.html")

@login_required
def create_listing(req):
    if req.method == "GET":
        categories = Category.objects.all()
        return render(req, "auctions/create.html", {
            "categories": categories
        })
    else:
        data = {
            "title": req.POST["title"],
            "description": req.POST["description"],
            "image": req.POST["image"],
            "price": req.POST["price"],
            "category": req.POST["category"],
            "owner": req.user
        }
        
        category = Category.objects.get(category_name = data["category"])
        
        new_listing = Listing(
            title=data["title"],
            description=data["description"],
            image=data["image"],
            price=float(data["price"]),
            category=category,
            owner=data["owner"],
        )
        new_listing.save()
        return HttpResponseRedirect(reverse(index))
    


def listing(req, listing_id):
    listing_data = Listing.objects.get(pk= listing_id)
    is_exist = False
    winner = listing_data.winner if not listing_data.is_active else None

    if isinstance(req.user, AnonymousUser):
        is_exist = False
    else:
        is_exist = listing_data in req.user.watchlist.all()
    
    return render(req, "auctions/listing.html", {
        "listing": listing_data,
        "is_exist": is_exist,
        "highest_bid": listing_data.current_highest_bid(),
        "comments": listing_data.comments.all(),
        "winner": winner
    })

@login_required
def handle_watchlist(req, listing_id):
    if req.method == 'POST':
        listing = Listing.objects.get(pk= listing_id)
        if listing in req.user.watchlist.all():
            req.user.watchlist.remove(listing)
        else:
            req.user.watchlist.add(listing)
    
    return redirect('listing', listing_id=listing_id)

@login_required
def handle_bid(req, listing_id):
    if req.method == 'POST':
        listing = Listing.objects.get(pk= listing_id)
        amount = float(req.POST.get('bid'))
        current_highest_bid = listing.current_highest_bid()
        winner = listing.winner if not listing.is_active else None
        
        if amount <= current_highest_bid:
            error = "Your bid must be higher than the current highest bid."
            
            return render(req, "auctions/listing.html", {
                "listing": listing,
                "is_exist": listing in req.user.watchlist.all(),
                "error": error,
                "highest_bid": current_highest_bid,
                "comments": listing.comments.all(),
                "winner": winner
            })
        
        Bid.objects.create(listing=listing, user=req.user, amount=amount)
        return redirect('listing', listing_id=listing_id)

@login_required
def add_comment(req, listing_id):
    if req.method == 'POST':
        listing = Listing.objects.get(pk= listing_id)
        comment = req.POST.get("comment")
        new_comment = Comment(listing=listing, user=req.user, content=comment)
        new_comment.save()
        return redirect('listing', listing_id=listing_id)

@login_required
def close(req, listing_id):
    if req.method == 'POST':
        listing = Listing.objects.get(pk= listing_id)
        if req.user == listing.owner:
            listing.is_active = False
            listing.winner = listing.get_winner()
            listing.save()
            return redirect('listing', listing_id=listing_id)
        else:
            return redirect('index')

@login_required
def open(req, listing_id):
    if req.method == 'POST':
        listing = Listing.objects.get(pk= listing_id)
        if req.user == listing.owner:
            listing.is_active = True
            listing.winner = None
            listing.save()
            return redirect('listing', listing_id=listing_id)
        else:
            return redirect('index')
        
@login_required
def delete(req, listing_id):
    if req.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        listing.delete()
        return redirect('index')
        

def watchlist(req):
    user = User.objects.get(pk= req.user.id)
    listings = user.watchlist.all()
    return render(req, "auctions/index.html", {
        "listings": listings,
        "type": "watchlist",
    })
    
def categories(req):
    categories = Category.objects.all()
    return render(req, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(req, category_id):
    category = Category.objects.get(pk=category_id)
    active_listings = Listing.objects.filter(category=category, is_active=True)
    return render(req, "auctions/category_listings.html", {
        "category": category,
        "listings": active_listings
    })