from Queue import Queue
import unittest
import vcr
from web_snake.crawler import Crawler
from web_snake.crawler_storage import CrawlerStorage
from web_snake.result_set import ResultSet


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.storage = CrawlerStorage('test_web_snake')

    def test_clean(self):
        q = Queue()
        crawler = Crawler(crawl_queue=q, result=q, crawled=self.storage, max_level=0)

        self.assertEqual(crawler.clean('http://www.google.com|2'), 'http://www.google.com')
        self.assertEqual(crawler.clean('http://www.google.com#dfgdfg'), 'http://www.google.com')

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_1.yaml')
    def test_crawl_with_max_level_1(self):
        crawl_queue = Queue()
        crawl_queue.put('http://dppiwapikalipasir.org/halkomentar-153-1469.html')

        result = ResultSet()

        crawler = Crawler(crawl_queue=crawl_queue, result=result, crawled=self.storage, max_level=1)
        crawler.start()
        crawler.join()
        self.assertTrue(len(result.all()) >= 2)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_2.yaml')
    def test_crawl_with_max_level_2(self):
        crawl_queue = Queue()
        crawl_queue.put('http://dppiwapikalipasir.org/halkomentar-153-1469.html')

        result = ResultSet()

        crawler = Crawler(crawl_queue=crawl_queue, result=result, crawled=self.storage, max_level=2)
        crawler.start()
        crawler.join()

        self.assertTrue(len(result.all()) >= 100)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_3.yaml')
    def test_crawl_with_max_level_3(self):
        crawl_queue = Queue()
        crawl_queue.put('http://dppiwapikalipasir.org/halkomentar-153-1469.html')

        result = ResultSet()

        crawler = Crawler(crawl_queue=crawl_queue, result=result, crawled=self.storage, max_level=3)
        crawler.start()
        crawler.join()

        self.assertTrue(len(result.all()) >= 1000)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_a_page_with_different_type_of_links.yaml')
    def test_crawl_a_page_with_different_type_of_links(self):
        crawl_queue = Queue()
        crawl_queue.put('http://www.dn.se/')

        result = ResultSet()

        crawler = Crawler(crawl_queue=crawl_queue, result=result, crawled=self.storage, max_level=1)
        crawler.start()
        crawler.join()

        self.assertTrue(len(result.all()) >= 100)

    def tearDown(self):
        self.storage.remove_all()