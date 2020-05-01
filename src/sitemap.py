from pathlib import Path
from datetime import datetime

class Sitemap:
    def __init__(self, base_url):
        self.urls = []
        self.base_url = str(base_url)

    def add_url(self, relative_url):
        self.urls.append(Url("/".join([self.base_url.strip("/"), str(relative_url).lstrip("/")]), f"{datetime.today():%Y-%m-%d}"))


class Url:
    def __init__(self, loc, lastmod):
        self.loc = loc
        self.lastmod = lastmod
