from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
