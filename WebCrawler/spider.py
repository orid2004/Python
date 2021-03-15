from urllib.request import urlopen
from gather_links import gather
from link_finder import LinkFinder


class Spider:
    base_url = None
    domain_name = None

    def __init__(self, base_url, domain_name):
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        self.crawl_page(Spider.base_url)

    @staticmethod
    def crawl_page(page_url):
        for link in Spider.gather_links(page_url):
            if Spider.domain_name in link:
                gather(link)

    @staticmethod
    def gather_links(page_url):
        try:
            response = urlopen(page_url)
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(e)
            return set()
        return finder.page_links()
