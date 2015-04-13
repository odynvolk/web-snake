from pymongo import MongoClient


class CrawlerStorage(object):
    def __init__(self, database_name='web_snake'):
        self.client = MongoClient()
        self.db = self.client[database_name]

    def count(self):
        self.db.crawled_urls.count()

    def insert(self, url):
        self.db.crawled_urls.insert({'url': url})

    def update(self, url):
        self.db.crawled_urls.update({'url': url}, {'url': url}, upsert=True)

    def find(self, url):
        result = self.db.crawled_urls.find({'url': url})
        if result.count() > 0:
            return [url for url in result]
        return None

    def remove_all(self):
        self.db.crawled_urls.remove({})