#!/usr/bin/env python3
import datetime
import sys
import time
from pathlib import Path
from shutil import ignore_patterns

from jinja2 import Environment, PackageLoader, select_autoescape
from markupsafe import Markup

from copytree import copytree
from find_publications import find_publications
from sitemap import Sitemap

BASE_URL = "https://lpr-ekb.ru/"


def main(args):
    is_release = "release" in args
    
    Path("../out/news").mkdir(parents=True, exist_ok=True)
    Path("../out/articles").mkdir(parents=True, exist_ok=True)
    copytree("./news", "../out/news", ignore=ignore_patterns("*.md"))
    copytree("./articles", "../out/articles", ignore=ignore_patterns("*.md"))

    news_list = find_publications("./news")
    article_list = find_publications("./articles")

    env = Environment(
        loader=PackageLoader("generate", "./templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    news_items = [
        {
            "title": Markup(news.render_title_link("/" + news.path.strip("/") + "/")),
            "date": format_date(news.date),
            "path": news.path,
        }
        for news in news_list
    ]

    sitemap = Sitemap(BASE_URL)
    sitemap.add_url("/")
    sitemap.add_url("/news/")

    for news in news_list:
        render_template(
            env,
            "news.html",
            f"../out/{news.path.strip('/')}/index.html",
            release=is_release,
            meta_title=news.render_title(),
            meta_description=news.description,
            meta_canonical=f'{BASE_URL.rstrip("/")}/{news.path.strip("/")}/',
            content=Markup(news.html),
            date=format_date(news.date),
            other_news=[on for on in news_items if news.path != on["path"]][:3],
        )

        sitemap.add_url(news.path)

    sitemap.add_url("/articles/")

    for article in article_list:
        render_template(
            env,
            "article.html",
            f"../out/{article.path.strip('/')}/index.html",
            release=is_release,
            meta_title=article.render_title(),
            meta_description=article.description,
            meta_canonical=f'{BASE_URL.rstrip("/")}/{article.path.strip("/")}/',
            content=Markup(article.html),
            news=news_items[:3]
        )

        sitemap.add_url(article.path)

    render_template(
        env,
        "news-index.html",
        "../out/news/index.html",
        release=is_release,
        news=news_items,
        meta_title="Новости",
        meta_description=(
            "Новости либертарианства и Либертарианской Партии России в Екатеринбурге и Свердловской области"
        ),
        meta_canonical=f'{BASE_URL.rstrip("/")}/news/',
    )

    render_template(
        env,
        "article-index.html",
        "../out/articles/index.html",
        release=is_release,
        meta_title="Статьи",
        meta_description=(
            "Статьи про либертарианство и политику в Екатеринбурге и Свердловской области"
        ),
        meta_canonical=f'{BASE_URL.rstrip("/")}/articles/',
    )

    render_template(
        env,
        "home.html",
        "../out/index.html",
        release=is_release,
        news=news_items[:3],
        meta_description=(
            "Выступаем за свободную экономику, независимое местное самоуправление, "
            "суверенитет личности и против цензуры в интернете. Присоединяйся!"
        ),
    )

    render_template(env, "sitemap.xml", "../out/sitemap.xml", urls=sitemap.urls)

    copytree("./static", "../out")


def render_template(env, template_name, destination, **kwargs):
    env.get_template(template_name).stream(
        **kwargs, static_version=int(time.time())
    ).dump(destination)


months = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
]


def format_date(date):
    result = [str(date.day), months[date.month - 1]]
    if datetime.date.today().year > date.year:
        result.append(str(date.year))

    return " ".join(result)


if __name__ == "__main__":
    main(sys.argv[1:])
