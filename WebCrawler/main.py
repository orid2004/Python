from spider import Spider
from domain import *
from setup import *
import threading
from gather_links import *
import time
from enum import Enum


class Settings(Enum):
    URL = "https://" + input("Project Url > https://")
    PROJ_NAME = '.'.join(URL.split('.')[1:])
    DOMAIN = get_domain_name(URL)
    OUT_FILE = PROJ_NAME + "/output.txt"


suspend: bool


def crawl():
    while True:
        link = to_crawl.get()
        try:
            Spider(link, Settings.DOMAIN.value)
        except Exception as e:
            print(e)


def update_files():
    global suspend
    while True:
        link = output.get()
        with open(Settings.OUT_FILE.value, "a", encoding="utf-8") as f:
            f.write(link)
            f.write("\n")
        print("Update! Crawled: " + link)
        suspend = False


def build_spiders():
    for _ in range(10):
        threading.Thread(target=crawl).start()
    threading.Thread(target=update_files).start()


def main():
    setup(Settings.PROJ_NAME.value)
    who_input(get_domain_name(Settings.URL.value), Settings.PROJ_NAME.value)
    # avoid errors, make sure setup is done before writing the files...
    time.sleep(1)
    # create spiders
    build_spiders()
    Spider(Settings.URL.value, Settings.DOMAIN.value)


if __name__ == '__main__':
    main()
