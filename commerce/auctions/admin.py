from django.contrib import admin
from .models import User, Bid, Comment, Listing, Watchlist
# Register your models here.

class UsertAdmin(admin.ModelAdmin):
    list_display = ("username", "email")

admin.site.register(User,UsertAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(Watchlist)