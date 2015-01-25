import unittest
import vcr
from web_snake.crawler import Crawler


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler()

    def test_clean(self):
        self.assertEqual(self.crawler.clean('http://www.google.com|2'), 'http://www.google.com')
        self.assertEqual(self.crawler.clean('http://www.google.com#dfgdfg'), 'http://www.google.com')

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_1.yaml')
    def test_crawl_with_max_level_1(self):
        self.assertTrue(len(self.crawler.crawl('http://dppiwapikalipasir.org/halkomentar-153-1469.html', 1)) >= 2)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_2.yaml')
    def test_crawl_with_max_level_1(self):
        self.assertTrue(len(self.crawler.crawl('http://dppiwapikalipasir.org/halkomentar-153-1469.html', 2)) >= 100)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_3.yaml')
    def test_crawl_with_max_level_1(self):
        self.assertTrue(len(self.crawler.crawl('http://dppiwapikalipasir.org/halkomentar-153-1469.html', 3)) >= 1000)
