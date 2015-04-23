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

crawl_queue = Queue()
crawl_queue.put('http://www.reddit.com/')

result_queue = Queue()

proxies = Proxies('../../commondata/proxies.txt')

crawler = Crawler(crawl_queue=crawl_queue, result_queue=result_queue, max_level=3, proxies=proxies)
crawler.start()
crawler.join()

print "Found {number} links...".format(number=result_queue.qsize())
```