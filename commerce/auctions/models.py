from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    choices=[("Toys","Toys"),("Electronics","Electronics"),("Mobiles","Mobiles")]
    title = models.CharField(max_length=64)
    description = models.TextField(blank=False)
    starting_bid = models.DecimalField(decimal_places=2,max_digits=100,default=20)
    img_url = models.URLField(blank=True,null=True)
    category = models.CharField(max_length=64,choices=choices,default="Toys")
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='goods')
    active = models.BooleanField(default=True)

    def __str__(self):
    	return f"{self.title}"



class Bid(models.Model):
    item = models.ForeignKey(Listing,on_delete=models.CASCADE)
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='bidder')
    winner = models.ForeignKey(User,on_delete=models.CASCADE, blank=True,null=True ,related_name='winner')
    current_bid = models.DecimalField(decimal_places=2,max_digits=100,default=20)

    def __str__(self):
        return f"bid on {self.item}"

class Comment(models.Model):
    item = models.ForeignKey(Listing,on_delete=models.CASCADE)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(blank=False)

    def __str__(self):
        return f"{self.customer}'s comment on {self.item}"

class Watchlist(models.Model):
    item = models.ManyToManyField(Listing)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)        
    
    def __str__(self):
        return f"{self.owner}'s Watchlist"
