import unittest
import vcr
from web_snake import WebSnake


class TestWebSnake(unittest.TestCase):
    def setUp(self):
        self.web_snake = WebSnake()

    def test_clean(self):
        self.assertEqual(self.web_snake.clean('http://www.google.com|2'), 'http://www.google.com')
        self.assertEqual(self.web_snake.clean('http://www.google.com#dfgdfg'), 'http://www.google.com')

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_1.yaml')
    def test_crawl_with_max_level_1(self):
        self.assertTrue(len(self.web_snake.crawl('http://dppiwapikalipasir.org/halkomentar-153-1469.html', 1)) >= 2)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_2.yaml')
    def test_crawl_with_max_level_1(self):
        self.assertTrue(len(self.web_snake.crawl('http://dppiwapikalipasir.org/halkomentar-153-1469.html', 2)) >= 100)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_3.yaml')
    def test_crawl_with_max_level_1(self):
        self.assertTrue(len(self.web_snake.crawl('http://dppiwapikalipasir.org/halkomentar-153-1469.html', 3)) >= 1000)
