from django.shortcuts import render
from django.http import HttpResponse
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_view(request, entry_name):
    print(util.get_entry(entry_name))
    return render(request, f"encyclopedia/layout.html", {
        "entries": util.get_entry(entry_name)
    })

