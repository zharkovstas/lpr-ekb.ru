#!/usr/bin/env python3
import sys
import time
from shutil import ignore_patterns
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
from markupsafe import Markup
from copytree import copytree
from find_news import find_news
from sitemap import Sitemap
import datetime

BASE_URL = "https://lpr-ekb.ru/"


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
            "title": Markup(n.render_title_link("/" + n.path.strip("/") + "/")),
            "date": format_date(n.date),
            "path": n.path
        }
        for n
        in news
    ]

    sitemap = Sitemap(BASE_URL)
    sitemap.add_url("/")
    sitemap.add_url("/news/")

    for n in news:

        render_template(
            env,
            "news.html",
            f"../out/{n.path.strip('/')}/index.html",
            release=is_release,
            meta_title=n.render_title(),
            meta_description=n.description,
            meta_canonical=f'{BASE_URL.rstrip("/")}/{n.path.strip("/")}/',
            content=Markup(n.html),
            date=format_date(n.date),
            other_news=[on for on in news_items if n.path != on["path"]][:3]
        )

        sitemap.add_url(n.path)

    render_template(
        env,
        "news-index.html",
        "../out/news/index.html",
        release=is_release,
        news=news_items,
        meta_title="Новости",
        meta_description="Новости либертарианства и Либертарианской Партии России в Екатеринбурге и Свердловской области",
        meta_canonical=f'{BASE_URL.rstrip("/")}/news/'
    )

    render_template(
        env,
        "home.html",
        "../out/index.html",
        release=is_release,
        news=news_items[:3],
        meta_description="""Выступаем за свободную экономику, независимое местное самоуправление,
суверенитет личности и против цензуры в интернете. Присоединяйся!""")

    render_template(env, "sitemap.xml",
                    "../out/sitemap.xml", urls=sitemap.urls)

    copytree("./static", "../out")


def render_template(env, template_name, destination, **kwargs):
    (env
        .get_template(template_name)
        .stream(**kwargs, static_version=int(time.time()))
        .dump(destination))


months = ["января", "февраля", "марта", "апреля", "мая", "июня",
          "июля", "августа", "сентября", "октября", "ноября", "декабря"]


def format_date(date):
    result = [str(date.day), months[date.month - 1]]
    if datetime.date.today().year > date.year:
        result.append(str(date.year))

    return " ".join(result)


if __name__ == "__main__":
    main(sys.argv[1:])
