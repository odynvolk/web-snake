import random
import re
import traceback
import urlparse
import collections
import ssl
from functools import wraps
import threading
from requests_futures.sessions import FuturesSession


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

session = FuturesSession(max_workers=10)


class Crawler(threading.Thread):
    def __init__(self, crawl_queue, result, crawled=None, max_level=3, proxies=None):
        threading.Thread.__init__(self)
        self.crawl_queue = crawl_queue
        self.crawled = crawled
        self.result = result
        self.max_level = max_level
        self.proxies = proxies

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
        if self.crawled.find_one_by_hash(cleaned_url):
            # print "Skipped: " + cleaned_url.decode('utf-8', 'ignore')
            return

        self.crawled.update(cleaned_url)

        try:
            proxy = {'http': random.choice(self.proxies)} if self.proxies else {}

            res = session.get(cleaned_url, headers=headers, timeout=30, proxies=proxy)

            resp = res.result()
            if resp.status_code != 200:
                return

            links = link_re.findall(resp.content)
            if links and isinstance(links, collections.Iterable):
                inner_links = [self.clean(urlparse.urljoin(cleaned_url, link)) for link in links]

                for link in links:
                    link = urlparse.urljoin(cleaned_url, link)
                    inner_result = self.crawl(link, max_level - 1)
                    if inner_result:
                        inner_links.expand([self.clean(inner_link) for inner_link in inner_result])

                self.result.put(inner_links)
        except:
            # print traceback.format_exc()
            pass

    def clean(self, url):
        idx = url.find('#')
        if idx > 0:
            return url[:idx]

        idx = url.find('|')
        if idx > 0:
            return url[:idx]

        return url