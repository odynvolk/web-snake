from Queue import Queue
import unittest
import vcr
from web_snake.crawler import Crawler


class TestCrawler(unittest.TestCase):
    def setUp(self):
        pass

    def test_clean(self):
        q = Queue()
        crawler = Crawler(crawl_queue=q, result_queue=q, max_level=0)

        self.assertEqual(crawler.clean('http://www.google.com|2'), 'http://www.google.com')
        self.assertEqual(crawler.clean('http://www.google.com#dfgdfg'), 'http://www.google.com')

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_1.yaml')
    def test_crawl_with_max_level_1(self):
        crawl_queue = Queue()
        crawl_queue.put('http://dppiwapikalipasir.org/halkomentar-153-1469.html')

        result_queue = set()

        crawler = Crawler(crawl_queue=crawl_queue, result_queue=result_queue, max_level=1)
        crawler.start()
        crawler.join()

        self.assertTrue(len(result_queue) >= 2)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_2.yaml')
    def test_crawl_with_max_level_2(self):
        crawl_queue = Queue()
        crawl_queue.put('http://dppiwapikalipasir.org/halkomentar-153-1469.html')

        result_queue = Queue()

        crawler = Crawler(crawl_queue=crawl_queue, result_queue=result_queue, max_level=2)
        crawler.start()
        crawler.join()

        self.assertTrue(result_queue.qsize() >= 100)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_3.yaml')
    def test_crawl_with_max_level_3(self):
        crawl_queue = Queue()
        crawl_queue.put('http://dppiwapikalipasir.org/halkomentar-153-1469.html')

        result_queue = Queue()

        crawler = Crawler(crawl_queue=crawl_queue, result_queue=result_queue, max_level=3)
        crawler.start()
        crawler.join()

        self.assertTrue(result_queue.qsize() >= 1000)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_a_page_with_different_type_of_links.yaml')
    def test_crawl_a_page_with_different_type_of_links(self):
        crawl_queue = Queue()
        crawl_queue.put('http://www.dn.se/')

        result_queue = Queue()

        crawler = Crawler(crawl_queue=crawl_queue, result_queue=result_queue, max_level=1)
        crawler.start()
        crawler.join()

        self.assertTrue(result_queue.qsize() >= 400)
