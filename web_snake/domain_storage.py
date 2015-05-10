from pymongo import MongoClient


class DomainStorage(object):
    def __init__(self, database_name='web_snake'):
        self.client = MongoClient()
        self.db = self.client[database_name]

    def count(self):
        self.db.crawled_domains.count()

    def inc(self, domains):
        if not domains:
            return

        bulkop = self.db.crawled_domains.initialize_ordered_bulk_op()
        for domain in domains:
            bulkop.find({'domain': domain}).upsert().update({"$inc": {"urls": 1}})
        bulkop.execute()

    def urls_for_domains(self, domains):
        result = {}
        for re in self.db.crawled_domains.find({'domain': {"$in": domains}}):
            result[re['domain']] = re['urls']

        for domain in domains:
            if not domain in result:
                result[domain] = 0

        return result

    def remove_all(self):
        self.db.crawled_domains.remove({})
