from scrapy import signals
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher

from LxScraper.LxScraper.spiders.scraper import Scraper
class WebScraper():
   
    def run_spider(self):
        results = []

        def crawler_results(signal, sender, item, response, spider):
            results.append(item)

        dispatcher.connect(crawler_results, signal=signals.item_scraped)

        process = CrawlerProcess(get_project_settings())
        process.crawl(Scraper)
        
        process.start()
        return results