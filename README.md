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

crawler = Crawler(url='http://www.reddit.com/', max_level=3)
crawler.start()
crawler.join()
crawler.urls
```