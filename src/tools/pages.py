import markdown
import re
from pathlib import Path
from markupsafe import Markup

from tools.files import read_all_text
from tools.texts import improve_text, add_nbsp, cut


class Page:
    def __init__(self, url, title, title_link_html, html, date, description):
        self.url = url
        self.title = title
        self.title_link_html = title_link_html
        self.html = html
        self.date = date
        self.description = description


def read_pages(path, process_html=None):
    pages = []

    for path in Path(path).rglob("*.md"):
        pages.append(read_page(path, process_html=process_html))

    return sorted(pages, key=lambda x: x.date, reverse=True)


def read_page(path, process_html=None):
    md = markdown.Markdown(extensions=["full_yaml_metadata"])
    text = read_all_text(path)
    title = find_title(text)
    improved_title = improve_text(title)
    cleaned_text = replace_title(
        text, remove_brackets(title)) if title else text
    improved_text = improve_text(cleaned_text)
    html = md.convert(cleaned_text)

    if process_html:
        html = process_html(html)

    url = "/" + str(Path(path).parent).rstrip("/") + "/"
    date = md.Meta["date"] if md.Meta else None

    return Page(
        url,
        remove_brackets(title),
        render_title_link(improved_title, url),
        Markup(html),
        date,
        cut(remove_specials(improved_text), 150),
    )


def find_title(text):
    match = re.search(r"^#([^#].*)", text, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def replace_title(text, new_title):
    return re.sub(r"^#([^#].*)", f"# {new_title}", text, flags=re.MULTILINE, count=1)


def remove_brackets(input):
    return re.sub(r"[\[\]]", "", input)


def render_title_link(title, url):
    return Markup(
        title.replace("[", f'<a href="{url}">').replace("]", "</a>")
        if "[" in title
        else f"<a href={url}>{title}</a>"
    )


def remove_specials(text):
    dots_index = text.find("...")
    text = text[dots_index:] if dots_index != -1 else text
    text = re.sub(r"^.*?\.\.\.", "", text)
    text = re.sub(r"^([#!\[\<]).*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"[\[\]]", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()
