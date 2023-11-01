from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher

from web_scraper.web_scraper.spiders.sreality import SrealitySpider
class WebScraperRunner():
   
    def run_spider(self):
        results = []

        def crawler_results(signal, sender, item, response, spider):
            results.append(item)

        dispatcher.connect(crawler_results, signal=signals.item_scraped)

        process = CrawlerProcess(get_project_settings())
        process.crawl(SrealitySpider)
        
        process.start()
        return results