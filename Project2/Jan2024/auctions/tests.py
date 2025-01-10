from django.test import TestCase

# Create your tests here.
class TestCalls(TestCase):
    def test_new_listing_deny_anonymouse(self):
        response = self.client.get("new_listing")
            self.assertRedirects(response, '/login/')
        response = self.client.


"""urlpatterns = [
path("", views.index, name="index"),
path("login", views.login_view, name="login"),
path("logout", views.logout_view, name="logout"),
path("register", views.register, name="register"),
path("new_listing", views.new_listing, name="new_listing"),
path("listing/<str:listing_title>", views.listing, name="listing"),
path("listing/<str:listing_title>/new_bid", views.new_bid, name="new_bid"),
path("listing/<str:listing_title>/new_comment", views.new_comment, name="new_comment"),
path("listing/<str:listing_title>/remove_listing", views.remove_listing, name="remove_listing"),

]

# If Debug Mode serve images from Django project
if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"""