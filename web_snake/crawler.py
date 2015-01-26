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

link_re = re.compile(r'<a href="(.*?)"')

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
           'Accept': 'text/plain'}


class Crawler(threading.Thread):
    def __init__(self, queue, max_level):
        threading.Thread.__init__(self)
        self.accessed = set()
        self.queue = queue
        self.max_level = max_level
        self.urls = []

    def run(self):
        while not self.queue.empty():
            self.urls.extend(self.crawl(self.queue.get(), self.max_level))
            self.queue.task_done()

    def crawl(self, url, max_level):
        cleaned_url = self.clean(url)
        if max_level == 0 or cleaned_url in self.accessed:
            return

        self.accessed.add(cleaned_url)

        result = set()

        try:
            req = requests.get(cleaned_url, headers=headers, timeout=30)
            if req.status_code != 200:
                return

            links = link_re.findall(req.text)
            if links and isinstance(links, collections.Iterable):
                [result.add(self.clean(urlparse.urljoin(cleaned_url, link))) for link in links]

                for link in links:
                    link = urlparse.urljoin(cleaned_url, link)
                    inner_result = self.crawl(link, max_level - 1)
                    if inner_result:
                        [result.add(self.clean(inner_link)) for inner_link in inner_result]
        except:
            pass

        return result

    def clean(self, url):
        idx = url.find('#')
        if idx > 0:
            return url[0:idx]

        idx = url.find('|')
        if idx > 0:
            return url[0:idx]

        return url