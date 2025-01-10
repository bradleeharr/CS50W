from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<str:listing_title>", views.listing, name="listing"),
    path("listing/<str:listing_title>/new_bid", views.new_bid, name="new_bid"),
    path("listing/<str:listing_title>/new_comment", views.new_comment, name="new_comment"),
    path("listing/<str:listing_title>/remove_listing", views.remove_listing, name="remove_listing"),
    path("listing/<str:listing_title>/add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),

]

# If Debug Mode serve images from Django project
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)