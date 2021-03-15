from html.parser import HTMLParser
from urllib import parse
from enum import Enum


class Syntax(Enum):
    LINK_TAG = 'a'
    HREF_ATT = "href"


class LinkFinder(HTMLParser):
    def __init__(self, url, page):
        super().__init__()
        self.url = url
        self.page_url = page
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == Syntax.LINK_TAG.value:
            for attribute, value in attrs:
                if attribute == Syntax.HREF_ATT.value:
                    output = parse.urljoin(self.url, value)
                    self.links.add(output)

    def page_links(self):
        return self.links

    def error(self, message):
        print('Error: ' + message)
