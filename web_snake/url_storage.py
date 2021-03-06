from datetime import datetime
import hashlib
from pymongo import MongoClient


class UrlStorage(object):
    def __init__(self, database_name='web_snake'):
        self.client = MongoClient()
        self.db = self.client[database_name]

    def count(self):
        self.db.crawled_urls.count()

    def insert(self, url):
        self.db.crawled_urls.insert({'url': url, 'hash': hashlib.md5(url).hexdigest(), 'last_visited': datetime.now()})

    def update(self, url):
        self.db.crawled_urls.update({'url': url},
                                    {'url': url,
                                     'hash': hashlib.md5(url).hexdigest(),
                                     'last_visited': datetime.now()},
                                    upsert=True)

    def find(self, url):
        result = self.db.crawled_urls.find({'url': url})
        if result.count() > 0:
            return [url for url in result]
        return None

    def find_one(self, url):
        return self.db.crawled_urls.find_one({'url': url})

    def find_one_by_hash(self, url):
        return self.db.crawled_urls.find_one({'hash': hashlib.md5(url).hexdigest()})

    def remove_all(self):
        self.db.crawled_urls.remove({})
