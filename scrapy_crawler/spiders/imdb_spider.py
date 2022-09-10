import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

class IMDBSpider(CrawlSpider):
    name = 'imdb_spider'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top']
    rules = [
        Rule(LinkExtractor(allow=('title/tt')), callback='parse', follow=False, cb_kwargs={'the_type':'250films'}),
    ]

    def parse(self, response, the_type):
        if the_type == "250films":
            yield {
                "Title" : response.css('h1::text')[0].get(),
                "Year" : response.css("span.TitleBlockMetaData__ListItemText-sc-12ein40-2::text").get(),
                "Director" : response.css("a.ipc-metadata-list-item__list-content-item::text").get(),
                "Actor" : response.xpath("//a[text()='Stars']/following-sibling::div//a//text()").get(),
                "Rate" : response.css("span.AggregateRatingButton__RatingScore-sc-1ll29m0-1::text").get(),
                "Depth Level": response.meta.get("depth"),
            }
