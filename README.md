# web-snake
A simple web crawler in Python that crawls and returns the urls.


# INSTALL

If you have downloaded the source code:

```bash
python setup.py install
```


## python

``` python
from web_snake.crawler import Crawler

crawl_queue = Queue()
crawl_queue.put('http://www.reddit.com/')

result_queue = Queue()

crawler = Crawler(crawl_queue=crawl_queue, result_queue=result_queue, max_level=3)
crawler.start()
crawler.join()

print "Found {number} links...".format(number=result_queue.qsize())
```