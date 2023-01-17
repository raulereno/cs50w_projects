from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    #My urls
    path("closelisting",views.close_listing,name="closedlisting"),
    path("createlisting",views.create_listing,name="createlisting"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("watchlist/<int:user_id>", views.watchList, name="watchlist"),
    path("<int:listing_id>/add", views.addWatchList, name="addwatchlist"),
    path("<int:listing_id>/remove", views.removeWatchList, name="removewatchlist"),
    path("<int:listing_id>/addbid", views.addBid, name="addbid"),
    path("<int:listing_id>/addcomment", views.addComment, name="addcomment"),
    path("<int:listing_id>/close_auction", views.close_auction, name="closeauction"),
    path("category/<str:category>", views.category, name="category")
]
