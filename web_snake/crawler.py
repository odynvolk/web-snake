import re
import traceback
from urlparse import urljoin
import collections
import ssl
from functools import wraps
import threading
from requests_futures.sessions import FuturesSession
from urlparse import urlparse


def ssl_wrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

ssl.wrap_socket = ssl_wrap(ssl.wrap_socket)


def parse_domain(url):
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)


def clean_url(url):
    idx = url.find('#')
    if idx > 0:
        return url[:idx]

    idx = url.find('|')
    if idx > 0:
        return url[:idx]

    return url


link_re = re.compile(r'<a\s*.*href="(.*?)"')

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
           'Accept': 'text/plain'}

session = FuturesSession(max_workers=10)


class Crawler(threading.Thread):
    def __init__(self, crawl_queue, result, domains=None, max_urls_per_domain=500, urls=None, max_level=3, proxies=None):
        threading.Thread.__init__(self)
        self.crawl_queue = crawl_queue
        self.domains = domains
        self.max_urls_per_domain = max_urls_per_domain
        self.urls = urls
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

        cleaned_url = clean_url(url)
        if self.urls.find_one_by_hash(cleaned_url):
            # print "Skipped: " + cleaned_url.decode('utf-8', 'ignore')
            return

        domain = parse_domain(cleaned_url)
        if self.domains and self.domains.urls_for_domains([domain])[domain] >= self.max_urls_per_domain:
            return

        self.urls.update(cleaned_url)

        try:
            proxy = {'http': self.proxies.random()} if self.proxies else {}

            res = session.get(cleaned_url, headers=headers, timeout=30, proxies=proxy)
            resp = res.result()
            if resp.status_code != 200:
                return

            links = link_re.findall(resp.content)

            if links and isinstance(links, collections.Iterable):
                inner_links = [clean_url(urljoin(cleaned_url, link)) for link in links]
                if self.domains:
                    inner_links = self.filter_urls(inner_links)

                for link in links:
                    link = urljoin(cleaned_url, link)
                    inner_result = self.crawl(link, max_level - 1)
                    if inner_result:
                        inner_links.expand([clean_url(inner_link) for inner_link in inner_result])

                self.result.put(inner_links)
        except:
            # print traceback.format_exc()
            pass

    def filter_urls(self, urls):
        result = []
        domains = [parse_domain(url) for url in urls]
        urls_for_domains = self.domains.urls_for_domains(domains)

        for idx, url in enumerate(urls):
            domain = domains[idx]
            if urls_for_domains[domain] < self.max_urls_per_domain:
                result.append(url)
                self.domains.inc(domain)

        return result
