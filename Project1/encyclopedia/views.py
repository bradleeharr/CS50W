from django.shortcuts import render
from django.http import HttpResponse
from . import util
import random

def parse_links(line):
    off = 0
    linked_line = ""
    while line[off:] is not None:
        a = line[off:].find('[')
        b = line[off:].find(']')
        c = line[off:].find('(')
        d = line[off:].find(')')

        if a == -1 or b == -1 or c == -1 or d == -1:
            linked_line += line[off:]
            break
        if c == b + 1:
            link_text = line[off + a + 1:off + b]
            link_link = line[off + c + 1:off + d]
            linked_line += line[off:off + a] + f"<a href={link_link}>{link_text}</a>"
        else:
            linked_line += line[off:off + d]
        off += d + 1
    return linked_line


def handleBullets(lines):
    in_list = False
    html_output = ""
    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith(('*', '-', '+')):
            # Bullet point line
            indent_level = len(line) - len(stripped_line)

            if not in_list:
                html_output += "<ul>" * indent_level
                in_list = True
                list_level = indent_level
            elif indent_level > list_level:
                html_output += "<ul>"
            elif indent_level < list_level:
                html_output += "</ul>"

            list_level = indent_level
            html_output += "<li>" + stripped_line[1:].strip() + "</li>"
        else:
            # Not a bullet point line
            if in_list:
                html_output += "</ul>" * list_level
                in_list = False
                list_level = 0
            html_output += "<p>" + stripped_line + "</p>"

    if in_list:
        html_output += "</ul>" * list_level

    return html_output


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_view(request, entry_name):
    markdown = util.get_entry(entry_name)
    idx = 0
    bolded = ""
    while idx < len(markdown):
        first_bold = markdown.find("**", idx)
        if first_bold == -1:
            bolded += markdown[idx:]
            break
        end_bold = markdown.find("**", first_bold+2)
        if end_bold == -1:
            bolded += markdown[idx:]
            break
        bolded += markdown[idx:first_bold] + "<b>" + markdown[first_bold+2:end_bold] + "</b>"
        idx = end_bold + 2
    markdown = bolded

    lines = markdown.split('\n')
    for idx, line in enumerate(lines):
        lines[idx] = parse_links(line)
        if line.startswith("#"):
            header_level = len(line) - len(line.lstrip('#'))
            header_content = line.lstrip('#').strip()
            lines[idx] = f"<h{header_level}>{header_content}</h{header_level}>"

    html_content = handleBullets(lines)
    print(html_content)
    return render(request, "encyclopedia/layout.html", {
        "markdown": html_content
    })


def search(request, search_name):
    return render(request, "encyclopedia/layout.html", {
        "markdown": "HIHIHI SEARCH PAGE HERE"
    })

def random_page(request):
    print("GETTING RANDOM PAGE: ", random.choice(util.list_entries()))
    return entry_view(request, random.choice(util.list_entries()))

