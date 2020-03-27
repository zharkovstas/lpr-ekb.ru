#!/usr/bin/env python3
from pathlib import Path
import markdown
import re


class News:
    def __init__(self, path, title, html, date):
        self.path = path
        self.title = title
        self.html = html
        self.date = date

    def render_title_link(self, url):
        return self.title.replace('[', f'<a href="{url}">').replace(']', '</a>') if "[" in self.title else f"<a href={url}>{self.title}</a>"

    def render_title(self):
        return remove_brackets(self.title)


def find_news():
    news_list = []

    for path in Path("./news").rglob("*.md"):
        md = markdown.Markdown(extensions=['full_yaml_metadata'])
        text = read_all_text(path)
        title = find_title(text)
        cleaned_text = replace_title(
            text, remove_brackets(title)) if title else text

        html = md.convert(cleaned_text)
        date = md.Meta["date"]
        news = News(path.parent, title, html, date)
        news_list.append(news)

    return sorted(news_list, key=lambda x: x.date, reverse=True)


def read_all_text(path):
    with open(path, 'r') as f:
        return f.read()


def find_title(text):
    match = re.search(r'^#([^#].*)', text, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def replace_title(text, new_title):
    return re.sub(r'^#([^#].*)', f"# {new_title}", text, flags=re.MULTILINE, count=1)


def remove_brackets(input):
    return re.sub(r'[\[\]]', '', input)


if __name__ == "__main__":
    find_news()
