import requests
import re
import urlparse
import collections
import ssl
from functools import wraps
import threading


def ssl_wrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

ssl.wrap_socket = ssl_wrap(ssl.wrap_socket)

link_re = re.compile(r'<a\s*.*href="(.*?)"')

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
           'Accept': 'text/plain'}


class Crawler(threading.Thread):
    def __init__(self, crawl_queue, result_queue, max_level):
        threading.Thread.__init__(self)
        self.accessed = set()
        self.crawl_queue = crawl_queue
        self.result_queue = result_queue
        self.max_level = max_level

    def run(self):
        while not self.crawl_queue.empty():
            url = self.crawl_queue.get()

            print "Doing: " + url.decode('utf-8', 'ignore')

            self.crawl(url, self.max_level)
            self.crawl_queue.task_done()

    def crawl(self, url, max_level):
        if max_level == 0:
            return

        cleaned_url = self.clean(url)
        if cleaned_url in self.accessed:
            return

        self.accessed.add(cleaned_url)

        try:
            req = requests.get(cleaned_url, headers=headers, timeout=30)
            if req.status_code != 200:
                return

            links = link_re.findall(req.text)
            if links and isinstance(links, collections.Iterable):
                [self.result_queue.put(self.clean(urlparse.urljoin(cleaned_url, link))) for link in links]

                for link in links:
                    link = urlparse.urljoin(cleaned_url, link)
                    inner_result = self.crawl(link, max_level - 1)
                    if inner_result:
                        [self.result_queue.put(self.clean(inner_link)) for inner_link in inner_result]
        except:
            pass

    def clean(self, url):
        idx = url.find('#')
        if idx > 0:
            return url[:idx]

        idx = url.find('|')
        if idx > 0:
            return url[:idx]

        return url