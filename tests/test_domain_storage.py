import unittest
from web_snake.domain_storage import DomainStorage


class TestCrawlerStorage(unittest.TestCase):
    def setUp(self):
        self.storage = DomainStorage('test_web_snake')

    def test_return_zero_when_not_found(self):
        self.assertEqual(0, self.storage.urls_for_domains(['http://www.gazeta.ru/'])['http://www.gazeta.ru/'])

    def test_return_one_when_one_crawled(self):
        self.storage.inc(['http://www.hownice.com/'])
        self.assertEqual(1, self.storage.urls_for_domains(['http://www.hownice.com/'])['http://www.hownice.com/'])

    def test_return_two_when_two_crawled(self):
        self.storage.inc(['http://www.bad.com/'])
        self.storage.inc(['http://www.bad.com/'])
        self.assertEqual(2, self.storage.urls_for_domains(['http://www.bad.com/'])['http://www.bad.com/'])

    def test_return_two_when_two_crawled_on_same_page(self):
        self.storage.inc(['http://www.bad2.com/', 'http://www.bad2.com/'])
        self.assertEqual(2, self.storage.urls_for_domains(['http://www.bad2.com/'])['http://www.bad2.com/'])

    def tearDown(self):
        self.storage.remove_all()
