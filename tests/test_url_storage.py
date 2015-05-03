import unittest
from web_snake.url_storage import UrlStorage


class TestUrlStorage(unittest.TestCase):
    def setUp(self):
        self.storage = UrlStorage('test_web_snake')

    def test_return_none_when_not_found(self):
        self.assertIsNone(self.storage.find_one('http://www.gazeta.ru/'))

    def test_read_and_write(self):
        self.storage.update('http://www.dn.se/')
        self.assertIsNotNone(self.storage.find_one('http://www.dn.se/'))
        self.assertIsNone(self.storage.find_one('http://www.dn.se/d'))

    def test_dont_add_duplicates(self):
        self.storage.update('http://www.expressen.se/')
        self.storage.update('http://www.expressen.se/')
        self.assertEqual(1, len(self.storage.find('http://www.expressen.se/')))

    def test_find_one_by_hash(self):
        self.storage.update('http://www.xyz.com/')
        self.assertIsNotNone(self.storage.find_one_by_hash('http://www.xyz.com/'))

    def test_dont_find_one_by_hash(self):
        self.assertIsNone(self.storage.find_one_by_hash('http://www.zyx.com/'))

    def tearDown(self):
        self.storage.remove_all()
