#!/usr/bin/env python3
import sys
from shutil import ignore_patterns
from tools import ensure_directory, copy_tree, TemplateRenderer, format_date, Sitemap, read_pages
from bs4 import BeautifulSoup

BASE_URL = "https://lpr-ekb.ru/"


def main(args):
    is_release = "release" in args

    ensure_directory("../out/news")
    ensure_directory("../out/articles")
    copy_tree("./news", "../out/news", ignore=ignore_patterns("*.md"))
    copy_tree("./articles", "../out/articles", ignore=ignore_patterns("*.md"))

    news_list = read_pages("./news", process_html=process_html)
    article_list = read_pages("./articles", process_html=process_html)

    renderer = TemplateRenderer("./templates")

    news_items = [
        {
            "title": news.title_link_html,
            "date": format_date(news.date),
            "url": news.url,
        }
        for news in news_list
    ]

    sitemap = Sitemap(BASE_URL)
    sitemap.add_url("/")
    sitemap.add_url("/news/")

    for news in news_list:
        renderer.render(
            "news.html",
            f"../out/{news.url.strip('/')}/index.html",
            release=is_release,
            meta_title=news.title,
            meta_description=news.description,
            meta_canonical=f'{BASE_URL.rstrip("/")}/{news.url.strip("/")}/',
            content=news.html,
            date=format_date(news.date),
            other_news=[
                on for on in news_items if news.url != on["url"]][:3],
        )

        sitemap.add_url(news.url)

    sitemap.add_url("/articles/")

    for article in article_list:
        renderer.render(
            "article.html",
            f"../out/{article.url.strip('/')}/index.html",
            release=is_release,
            meta_title=article.title,
            meta_description=article.description,
            meta_canonical=f'{BASE_URL.rstrip("/")}/{article.url.strip("/")}/',
            content=article.html,
            news=news_items[:3]
        )

        sitemap.add_url(article.url)

    renderer.render(
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

    renderer.render(
        "article-index.html",
        "../out/articles/index.html",
        release=is_release,
        meta_title="Статьи",
        meta_description=(
            "Статьи про либертарианство и политику в Екатеринбурге и Свердловской области"
        ),
        meta_canonical=f'{BASE_URL.rstrip("/")}/articles/',
    )

    renderer.render(
        "home.html",
        "../out/index.html",
        release=is_release,
        news=news_items[:3],
        meta_description=(
            "Выступаем за свободную экономику, независимое местное самоуправление, "
            "суверенитет личности и против цензуры в интернете. Присоединяйся!"
        ),
    )

    renderer.render("sitemap.xml", "../out/sitemap.xml", urls=sitemap.urls)

    copy_tree("./static", "../out")


def process_html(html):
    soup = BeautifulSoup(html, features="html.parser")

    for img in soup.find_all("img"):
        img["title"] = img["alt"]
        img["class"] = "img-fluid news-page-content-media"

    for iframe in soup.find_all("iframe"):
        iframe["class"] = "news-page-content-media"

    for h1 in soup.find_all("h1"):
        h1["class"] = "news-page-content-h1"

    for a in soup.find_all("a"):
        if a["href"].startswith("http"):
            a["target"] = "_blank"
            a["rel"] = "noopener"

    return str(soup)


if __name__ == "__main__":
    main(sys.argv[1:])
