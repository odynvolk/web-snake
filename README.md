# web-snake
A simple web crawler in Python that crawls and returns the urls.


# INSTALL

If you have downloaded the source code:

```bash
python setup.py install
```


## python

``` python
from Queue import Queue
from web_snake.crawler import Crawler
from web_snake.proxies import Proxies
from web_snake.domain_storage import DomainStorage
from web_snake.url_storage import UrlStorage
from web_snake.result_set import ResultSet


crawl_queue = Queue()
crawl_queue.put('http://www.reddit.com/')

result = ResultSet()

proxies = Proxies('../../commondata/proxies.txt')

urls = UrlStorage()
domains = DomainStorage()

crawler = Crawler(crawl_queue=crawl_queue, result=result, domains=domains, urls=urls, max_level=3, proxies=proxies)
crawler.start()
crawler.join()

print "Found {number} links...".format(number=result_queue.qsize())
```