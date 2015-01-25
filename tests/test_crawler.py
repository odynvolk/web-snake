import unittest
import vcr
from web_snake.crawler import Crawler


class TestCrawler(unittest.TestCase):
    def setUp(self):
        pass

    def test_clean(self):
        crawler = Crawler('', 3)

        self.assertEqual(crawler.clean('http://www.google.com|2'), 'http://www.google.com')
        self.assertEqual(crawler.clean('http://www.google.com#dfgdfg'), 'http://www.google.com')

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_1.yaml')
    def test_crawl_with_max_level_1(self):
        crawler = Crawler('http://dppiwapikalipasir.org/halkomentar-153-1469.html', 1)
        crawler.start()
        crawler.join()
        self.assertTrue(len(crawler.urls) >= 2)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_2.yaml')
    def test_crawl_with_max_level_2(self):
        crawler = Crawler('http://dppiwapikalipasir.org/halkomentar-153-1469.html', 2)
        crawler.start()
        crawler.join()
        self.assertTrue(len(crawler.urls) >= 100)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_3.yaml')
    def test_crawl_with_max_level_3(self):
        crawler = Crawler('http://dppiwapikalipasir.org/halkomentar-153-1469.html', 3)
        crawler.start()
        crawler.join()
        self.assertTrue(len(crawler.urls) >= 1000)
