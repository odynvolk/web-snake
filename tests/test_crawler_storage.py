import unittest
from web_snake.crawler_storage import CrawlerStorage


class TestCrawlerStorage(unittest.TestCase):
    def setUp(self):
        self.storage = CrawlerStorage('test_web_snake')

    def test_return_none_when_not_found(self):
        self.assertIsNone(self.storage.find('http://www.gazeta.ru/'))

    def test_read_and_write(self):
        self.storage.update('http://www.dn.se/')
        self.assertIsNotNone(self.storage.find('http://www.dn.se/'))

    def test_dont_add_duplicates(self):
        self.storage.update('http://www.expressen.se/')
        self.storage.update('http://www.expressen.se/')
        self.assertEqual(1, len(self.storage.find('http://www.expressen.se/')))

    def tearDown(self):
        self.storage.remove_all()
