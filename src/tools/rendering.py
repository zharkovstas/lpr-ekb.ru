import time
from tools.copytree import copytree
from jinja2 import Environment, PackageLoader, select_autoescape

class TemplateRenderer:
    def __init__(self, templates_path):
        self.env = Environment(
            loader=PackageLoader("generate", "./templates"),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def render(self, template_name, destination, **kwargs):
        self.env.get_template(template_name).stream(
            **kwargs, static_version=int(time.time())
        ).dump(destination)
