from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listing, Bid, Comment, Watchlist


class CreateListingForm(forms.Form):
    CHOICES=[("Toys","Toys"),("Electronics","Electronics"),("Mobiles","Mobiles")]
    title = forms.CharField(label='title', max_length=100,required=True)
    description = forms.CharField(label='listing description', max_length=100,required=True)
    starting_bid = forms.IntegerField()
    img_url = forms.URLField(label='image url', required=False)
    category = forms.ChoiceField(choices=CHOICES) 
            


def index(request):
    listings = Listing.objects.all()
    if Listing.objects.filter(active=True).count() == 0 :
        listings = []
    return render(request, "auctions/index.html", {
        "listings":listings,
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
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def create(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            img_url = form.cleaned_data["img_url"]
            category = form.cleaned_data["category"]
            owner = request.user
            Listing.objects.create(title=title, description= description,
                starting_bid=starting_bid, img_url=img_url, category=category,
                owner=owner)

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
    else:
        return render(request, "auctions/create.html", {
                "form": CreateListingForm()
            })

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
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listings(request,id):
    listing = Listing.objects.get(id=id)
    if  not Bid.objects.filter(item=listing) :
        current_bid = None        
    else :
        current_bid = Bid.objects.get(item=listing)
    comments= Comment.objects.filter(item=listing)
    return render(request, "auctions/listing.html",{
        "listing":listing, "current_bid":current_bid, "comments":comments
        })


def category_view(request,category):
    listings = Listing.objects.filter(category=category)
    if Listing.objects.filter(category=category,active=True).count() == 0 :
        listings = []
    return render(request, "auctions/category.html", {
        "listings":listings,
        })


def close_auction(request,listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.active = False
    listing.save()
    b = Bid.objects.get(item=listing)
    b.winner = b.customer
    b.save()
    return HttpResponseRedirect(reverse("listings", args=(listing_id,)))


def categories_view(request):
    categories= Listing.choices
    return render(request, "auctions/categories.html", {
        "categories":categories,
        })


@login_required
def add_to_watchlist(request, listing_id):
    customer = request.user
    item = Listing.objects.get(pk=listing_id)
    if not Watchlist.objects.filter(owner=customer) :
            w= Watchlist.objects.create(owner=customer)
            w.save()
            w.item.add(item)
    else:
        w= Watchlist.objects.get(owner=customer)
        w.item.add(item)
        w.save()
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def watchlist(request):
    if not Watchlist.objects.filter(owner=request.user) :
        listings = []
    else :
        w = Watchlist.objects.get(owner=request.user)
        listings = w.item.all()

    return render(request, "auctions/watchlist.html", {
        "listings":listings,
        })


@login_required
def bid(request,listing_id):
    if request.method == "POST":

        user_bid = round(float(request.POST["user_bid"]),2)
        customer = request.user
        item = Listing.objects.get(id=listing_id)
        message = False
        if user_bid <= item.starting_bid and not Bid.objects.filter(item=item):
            comments= Comment.objects.filter(item=item)
            message = True
            current_bid = []
            return render(request, "auctions/listing.html",
                {
                "listing":item, "current_bid": current_bid, "comments":comments,
                "message": message
                })        
        # create a bid if there isn't one already
        if not Bid.objects.filter(item=item) :
            b= Bid.objects.create(item=item, customer=customer, current_bid= user_bid)
            b.save()
        #check if user bid is higher than current bid :  

        current_bid = Bid.objects.get(item=item)
        if user_bid > current_bid.current_bid :
            current_bid.current_bid = user_bid
            current_bid.customer = customer
            current_bid.save()
            return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
        else:
            comments= Comment.objects.filter(item=item)
            message = True
            current_bid = current_bid
            return render(request, "auctions/listing.html",
                {
                "listing":item, "current_bid": current_bid, "comments":comments,
                "message": message
                })
    else :
        return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
@login_required
def comment_view(request,listing_id):
    if request.method == "POST":
        customer = User.objects.get(id=int(request.POST["user_id"]))
        content = request.POST["content"]
        item = Listing.objects.get(id=listing_id)
        c= Comment.objects.create(customer=customer, item=item, content=content)
        c.save()
        
        return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
