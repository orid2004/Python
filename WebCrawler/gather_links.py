import queue

output = queue.Queue()
to_crawl = queue.Queue()
output_set = set()


def gather(link):
    exists = 0
    for d in output_set:
        if d == link:
            exists = 1
    if exists == 0:
        output.put(link)
        output_set.add(link)
        to_crawl.put(link)
