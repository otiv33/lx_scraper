from typing import Any
import scrapy
from scrapy.http import Response
from playwright.sync_api import sync_playwright

class SrealitySpider(scrapy.Spider):
    name = 'SrealitySpider'
    url = 'https://www.sreality.cz'
    initial_url = url + '/en/search/for-sale/apartments'
    counter = 0
    max_number_of_items = 500
    
    def start_requests(self):
        yield self.make_request(self.initial_url)
    
    def parse(self, response: Response, **kwargs: Any) -> Any:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(response.url)

            page.wait_for_load_state("load")
            html_content = page.content()
            sel = scrapy.Selector(text=html_content)
            propertyList = sel.css('div.dir-property-list div.property')
            
            try:
                for property in propertyList:
                    title = property.css('div.info div span h2 a span::text').get()
                    image = property.css('preact div div:first-child a:first-child img::attr(src)').get()      
                    yield {
                        'title': title,
                        'image': image
                    }
                    self.counter += 1
                    if(self.counter >= self.max_number_of_items):
                        browser.close()
                        return
            except Exception as e:
                print(e)

            next_url = sel.css('.btn-paging-pn.icof.icon-arr-right.paging-next::attr(href)').get()
            if next_url is not None:
                next_page_url = self.url + next_url
                yield self.make_request(next_page_url)
    
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
        
    def make_request(self, target_url):
        return scrapy.Request(target_url, meta=dict(
                playwright = True,
                playwright_include_page = True,
                errback=self.errback,
            ),
        )