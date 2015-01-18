import unittest
from web_snake import WebSnake


class TestWebSnake(unittest.TestCase):
    def setUp(self):
        self.web_snake = WebSnake()

    def test_clean(self):
        self.assertEqual(self.web_snake.clean('http://www.google.com|2'), 'http://www.google.com')
        self.assertEqual(self.web_snake.clean('http://www.google.com#dfgdfg'), 'http://www.google.com')

    def test_crawl_with_max_level_1(self):
        self.assertTrue(len(self.web_snake.crawl('http://dppiwapikalipasir.org/halkomentar-153-1469.html', 1)) >= 2)