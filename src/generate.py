#!/usr/bin/env python3
import sys
from shutil import ignore_patterns
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
from markupsafe import Markup
from copytree import copytree
from find_news import find_news
import datetime


def main(args):
    is_release = "release" in args

    Path("../out/news").mkdir(parents=True, exist_ok=True)
    copytree("./news", "../out/news", ignore=ignore_patterns("*.md"))

    news = find_news()

    env = Environment(
        loader=PackageLoader('generate', './templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    news_items = [
        {
            "title": Markup(n.render_title_link(Path("/") / n.path)),
            "date": format_date(n.date),
            "path": n.path
        }
        for n
        in news
    ]

    news_template = env.get_template('news.html')

    for n in news:
        (news_template
         .stream(
             release=is_release,
             meta_title=n.render_title(),
             content=Markup(n.html),
             date=format_date(n.date),
             other_news=[on for on in news_items if n.path != on["path"]][:3])
         .dump(str(Path("../out") / n.path / "index.html")))

    (env
     .get_template('news-index.html')
     .stream(release=is_release, news=news_items, meta_title="Новости")
     .dump("../out/news/index.html"))

    (env
     .get_template('home.html')
     .stream(
         release=is_release,
         news=news_items[:3],
         meta_description="Выступаем за свободную экономику, независимое местное самоуправление, суверенитет личности и против цензуры в интернете. Присоединяйся!")
     .dump("../out/index.html"))

    copytree("./static", "../out")


months = ["января", "февраля", "марта", "апреля", "мая", "июня",
          "июля", "августа", "сентября", "октября", "ноября", "декабря"]


def format_date(date):
    result = [str(date.day), months[date.month - 1]]
    if datetime.date.today().year > date.year:
        result.append(str(date.year))

    return " ".join(result)


if __name__ == "__main__":
    main(sys.argv[1:])
