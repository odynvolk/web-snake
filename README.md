# web-snake
A simple web crawler in Python that crawls and returns the urls.


# INSTALL

If you have downloaded the source code:

```bash
python setup.py install
```


## python

``` python
from web_snake import WebSnake

web_snake = WebSnake()
links = web_snake.crawl(url='http://www.reddit.com/', max_level=1)
```