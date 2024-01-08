from django.shortcuts import render
from django.http import HttpResponse
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_view(request, entry_name):
    markdown = util.get_entry(entry_name)
    lines = markdown.split('\n')

    stack = []
    for idx, line in enumerate(lines):
        if line.startswith("#"):
            header_level = len(line) - len(line.lstrip('#'))
            header_content = line.lstrip('#').strip()
            lines[idx] = f"<h{header_level}>{header_content}</h{header_level}>"
        for cidx, char in enumerate(line):
            if char == '[':  # Start of Link
                link_text = line[cidx+1:]
                end_idx = link_text.index(']')
                link_text = link_text[:end_idx]
                print(link_text)





    html_content = lines
    return render(request, "encyclopedia/layout.html", {
        "markdown": html_content
    })


