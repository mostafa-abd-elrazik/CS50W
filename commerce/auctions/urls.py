from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add/<int:listing_id>", views.add_to_watchlist, name="add"),
    path("listings/<int:id>", views.listings, name="listings"),
    path("category/<str:category>", views.category_view, name="category"),
    path("create", views.create, name="create"),
    path("close/<int:listing_id>", views.close_auction, name="close_auction"),
    path("categories", views.categories_view, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment_view, name="comment"),
]
