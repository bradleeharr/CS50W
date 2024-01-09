from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
from . import mymarkdown
import random

from .util import save_entry



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_view(request, entry_name):
    markdown = util.get_entry(entry_name)
    markdown = mymarkdown.handleBold(markdown)
    markdown = mymarkdown.handleItal(markdown)

    lines = markdown.split('\n')
    for idx, line in enumerate(lines):
        lines[idx] = mymarkdown.parse_links(line)
        if line.startswith("#"):
            header_level = len(line) - len(line.lstrip('#'))
            header_content = line.lstrip('#').strip()
            lines[idx] = f"<h{header_level}>{header_content}</h{header_level}>"

    html_content = mymarkdown.handleBullets(lines)
    print(html_content)
    return render(request, "encyclopedia/layout.html", {
        "title": entry_name,
        "markdown": html_content
    })


def search(request):
    query = request.GET.get('q', '')
    results = []
    for entry in util.list_entries():
        if query.lower() in entry.lower():
            results.append(entry)
    return render(request, "encyclopedia/search.html", {
        "entries": results,
        "query": query
    })

def random_page(request):
    print("GETTING RANDOM PAGE: ", random.choice(util.list_entries()))
    return redirect('entry_detail', entry_name=random.choice(util.list_entries()))

def newpage(request):
    if request.method == 'POST':
        article_name = request.POST.get('n', '')
        if article_name in random.choice(util.list_entries()):
            error_message = "<h1>Page already exists</h1><p>The requested page already exists.</p>"
            return HttpResponse(error_message, status=409)  # 409 Conflict status code

        article_content = request.POST.get('content', '')
        save_entry(title=article_name, content=article_content)
        print("SAVED PAGE:")
        return entry_view(request, article_name)
        #return redirect('entry_detail', entry_detail=article_name)  # Replace 'page_detail' with your page detail view name

    print("GETTING NEW PAGE")
    return render(request, "encyclopedia/newpage.html", {})

def editpage(request, entry_name):
    entry_content = util.get_entry(entry_name)
    if request.method == 'POST':
        article_content = request.POST.get('content', '')
        save_entry(title=entry_name, content=article_content)
        print("SAVED EDITED PAGE:")
        return entry_view(request, entry_name)

    #return redirect('entry_detail', entry_detail=article_name)  # Replace 'page_detail' with your page detail view name

    print("GETTING NEW PAGE")
    return render(request, "encyclopedia/editpage.html", {
        "title" : entry_name,
        "content": entry_content
    })
