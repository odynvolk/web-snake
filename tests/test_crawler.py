from Queue import Queue
import unittest
import vcr
from web_snake.crawler import Crawler, parse_domain, clean_url
from web_snake.domain_storage import DomainStorage
from web_snake.url_storage import UrlStorage
from web_snake.result_set import ResultSet


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.urls = UrlStorage('test_web_snake')
        self.domains = DomainStorage('test_web_snake')

    def test_clean(self):
        self.assertEqual(clean_url('http://www.google.com|2'), 'http://www.google.com')
        self.assertEqual(clean_url('http://www.google.com#dfgdfg'), 'http://www.google.com')

    def test_filter_domain(self):
        self.assertEqual('http://www.whatever.com/', parse_domain('http://www.whatever.com/haha/haha'))
        self.assertEqual('http://www.whatever.com/', parse_domain('http://www.whatever.com/haha/haha?a=1'))
        self.assertEqual('http://www.whatever.com/', parse_domain('http://www.whatever.com/?a=1'))

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_1.yaml')
    def test_crawl_with_max_level_1(self):
        crawl_queue = Queue()
        crawl_queue.put('http://dppiwapikalipasir.org/halkomentar-153-1469.html')

        result = ResultSet()

        crawler = Crawler(crawl_queue=crawl_queue, result=result, urls=self.urls, max_level=1)
        crawler.start()
        crawler.join()

        self.assertTrue(len(result.all()) >= 2)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_2.yaml')
    def test_crawl_with_max_level_2(self):
        crawl_queue = Queue()
        crawl_queue.put('http://dppiwapikalipasir.org/halkomentar-153-1469.html')

        result = ResultSet()

        crawler = Crawler(crawl_queue=crawl_queue, result=result, urls=self.urls, max_level=2)
        crawler.start()
        crawler.join()

        self.assertTrue(len(result.all()) >= 100)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_max_level_3.yaml')
    def test_crawl_with_max_level_3(self):
        crawl_queue = Queue()
        crawl_queue.put('http://dppiwapikalipasir.org/halkomentar-153-1469.html')

        result = ResultSet()

        crawler = Crawler(crawl_queue=crawl_queue, result=result, urls=self.urls, max_level=3)
        crawler.start()
        crawler.join()

        self.assertTrue(len(result.all()) >= 1000)

    @vcr.use_cassette('fixtures/vcr_cassettes/crawl_a_page_with_different_type_of_links.yaml')
    def test_crawl_a_page_with_different_type_of_links(self):
        crawl_queue = Queue()
        crawl_queue.put('http://www.dn.se/')

        result = ResultSet()

        crawler = Crawler(crawl_queue=crawl_queue, result=result, urls=self.urls, max_level=1)
        crawler.start()
        crawler.join()

        self.assertTrue(len(result.all()) >= 100)

    @vcr.use_cassette('fixtures/vcr_cassettes/dont_crawl_more_pages_if_max_reached_on_page.yaml')
    def test_dont_crawl_more_pages_if_max_reached_on_page(self):
        crawl_queue = Queue()
        crawl_queue.put('https://www.pinterest.com/')
        crawl_queue.put('https://www.pinterest.com/jyldbd2/')
        crawl_queue.put('https://www.pinterest.com/class2290/')

        result = ResultSet()

        crawler = Crawler(crawl_queue=crawl_queue, result=result, domains=self.domains, max_urls_per_domain=5,
                          urls=self.urls, max_level=2)
        crawler.start()
        crawler.join()
        self.assertTrue(len(result.all()) == 90)
        self.assertEqual(21, self.domains.urls_for_domains(['https://www.pinterest.com/'])['https://www.pinterest.com/'])

    def tearDown(self):
        self.urls.remove_all()
        self.domains.remove_all()