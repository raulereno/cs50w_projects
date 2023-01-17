from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User,Listing,WatchList,Bid,Comment

class NewBidForm(forms.Form):
    bid = forms.DecimalField(label="",min_value=1,widget=forms.TextInput(attrs={'placeholder': 'Enter a bid'}) )

class NewListingForm(forms.Form):
    title = forms.CharField(max_length=25,label="",widget=forms.TextInput(attrs={'placeholder': 'Title'}) )
    description = forms.CharField(label="",widget=forms.Textarea(attrs={"rows":"5","placeholder":"Enter a description","class":"description"}))
    startPrice = forms.DecimalField(min_value=1,label="",widget=forms.TextInput(attrs={'placeholder': 'Start price'}) )
    url_img = forms.CharField(max_length=300,label="",widget=forms.TextInput(attrs={'placeholder': 'Url image'}) )
    category = forms.CharField(max_length=30,label="",widget=forms.TextInput(attrs={'placeholder': 'Category'}) )
    
class NewCommentForm(forms.Form):
    comment = forms.CharField(label='',max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Comment the article'}))

def getCategories():
    return sorted(set(list(Listing.objects.values_list('category',flat=True))))


def index(request):
    listings= Listing.objects.all().filter(sold=False)
    
    return render(request, "auctions/index.html",{
        "listings": listings,
        "categories":getCategories()
    })
    
def close_listing(request):
    listings= Listing.objects.all().filter(sold=True)
    
    return render(request, "auctions/index.html",{
        "listings": listings,
        "closed":True,
        "categories":getCategories()
    })
    
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html",{
            "categories":getCategories()
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            watchlist = WatchList.objects.create(user=user)
            watchlist.save()
            
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html",{
            "categories":getCategories()
        })

def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            newArticle = form.cleaned_data
            print(newArticle)
            article = Listing(title=newArticle['title'],description=newArticle['description'],startBid=newArticle['startPrice'],img=newArticle['url_img'],category=newArticle['category'],owner= request.user)
            article.save()
            return HttpResponseRedirect(reverse("index"))
            
    return render(request,"auctions/createListing.html",{
            "form":NewListingForm
    })

def listing(request,listing_id):
    
    listing = Listing.objects.get(pk= listing_id)
    isInWatchlist= False
    
    if request.user.is_authenticated is not False:
        watchlist = list(WatchList.objects.get(user = request.user).watchlist.all()) 
        for item in watchlist:
            isInWatchlist = True if item == listing else False
    
    return render(request, "auctions/listing.html",{
        "listing":listing,
        "bids":listing.bid.all(),
        "comments":listing.comment.all(),
        "watchlist":isInWatchlist,
        "formBid":NewBidForm(),
        "formComment":NewCommentForm(),
        "owner":listing.owner == request.user,
        "categories":getCategories()
    })
    
def watchList(request,user_id):
    try:
        watchlist = WatchList.objects.get(user_id = user_id)
        listing = Listing.objects.filter(item_watchlist = watchlist.id).all()
    except:
        watchlist = ""
        listing= []         
    
    return render(request, "auctions/watchlist.html",{
        "watchlist":watchlist,
        "listing":listing,
        "categories":getCategories()
    })
    
def addWatchList(request, listing_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            listing = Listing.objects.get(pk = listing_id)
            watchlist = WatchList.objects.get(user_id = request.user)
            watchlist.watchlist.add(listing)
        
            return HttpResponseRedirect(reverse("listing",args=[listing_id]))
        else:
            return HttpResponseRedirect(reverse("login"))
      
    
def removeWatchList(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = listing_id)
        watchlist = WatchList.objects.get(user_id = request.user)
        watchlist.watchlist.remove(listing)
        
        return HttpResponseRedirect(reverse("listing",args=[listing_id]))
    
def addBid(request,listing_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = NewBidForm(request.POST)
            newBid = float(request.POST['bid'])
            listing = Listing.objects.get(pk=listing_id)
            
            if newBid > listing.startBid:
                Bid.objects.create(price=newBid,listing=listing,user= request.user)
                listing.startBid = newBid
                listing.save()
                return HttpResponseRedirect(reverse("listing",args=[listing_id]))
            else:
                form.add_error('bid',f"Your bid should be higher than {listing.startBid}")
                
                watchlist= False
                
                for item in WatchList.objects.get(user_id=request.user).watchlist.all():
                    if item == listing:
                        watchlist=True
                    
                
                return render(request, "auctions/listing.html",{
                    "listing":listing,
                    "bids":listing.bid.all(),
                    "comments":listing.comment.all(),
                    "watchlist":watchlist,
                    "formBid":form,
                    "categories":getCategories()
                })
        else:
            return HttpResponseRedirect(reverse("login"))

def addComment(request,listing_id):
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            newComment = form.cleaned_data['comment']
            listing = Listing.objects.get(pk=listing_id)
            Comment.objects.create(text=newComment,listing=listing,user=request.user)
            return HttpResponseRedirect(reverse("listing",args=[listing_id]))    
        else:
            
            watchlist= False
            
            for item in WatchList.objects.get(user_id=request.user).watchlist.all():
                if item == listing:
                    watchlist=True
                    
            return render(request, "auctions/listing.html",{
                    "listing":listing,
                    "bids":listing.bid.all(),
                    "comments":listing.comment.all(),
                    "watchlist":watchlist,
                    "formBid":form,
                    "categories":getCategories()
                })    
        
              
def close_auction(request,listing_id):
    listing = Listing.objects.get(pk=listing_id)
    highestBid = Bid.objects.filter(listing=listing_id).order_by('price').reverse().first()
    
    if listing.owner == request.user:
        listing.sold=True
        listing.owner= highestBid.user
        listing.save()
        return HttpResponseRedirect(reverse("index"))
             
    
def category(request,category):
    listings = Listing.objects.filter(category=category)
    
    return render(request, "auctions/category.html",{
        "listings": listings,
        "category": category,
        "categories":getCategories()
    })