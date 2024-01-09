def handleItal(markdown):
    idx = 0
    ital = ""
    while idx < len(markdown):
        first_und = markdown.find("_", idx)
        if first_und == -1:
            ital += markdown[idx:]
            break
        end_und = markdown.find("_", first_und + 1)
        if end_und == -1:
            ital += markdown[idx:]
            break
        ital += markdown[idx:first_und] + "<em>" + markdown[first_und + 1:end_und] + "</em>"
        idx = end_und + 1
    return ital

def handleBold(markdown):
    idx = 0
    bolded = ""
    while idx < len(markdown):
        first_bold = markdown.find("**", idx)
        if first_bold == -1:
            bolded += markdown[idx:]
            break
        end_bold = markdown.find("**", first_bold + 2)
        if end_bold == -1:
            bolded += markdown[idx:]
            break
        bolded += markdown[idx:first_bold] + "<b>" + markdown[first_bold + 2:end_bold] + "</b>"
        idx = end_bold + 2
    return bolded


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