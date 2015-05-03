from pymongo import MongoClient


class DomainStorage(object):
    def __init__(self, database_name='web_snake'):
        self.client = MongoClient()
        self.db = self.client[database_name]

    def count(self):
        self.db.crawled_domains.count()

    def inc(self, domain):
        self.db.crawled_domains.update({'domain': domain},
                                        {"$inc": {"urls": 1}},
                                        upsert=True)

    def urls_for_domain(self, domain):
        res = self.db.crawled_domains.find_one({'domain': domain})
        if res:
            return res['urls']

        return 0

    def remove_all(self):
        self.db.crawled_domains.remove({})
