import scrapy
import scrapy.log

from scrapy.log import ERROR, WARNING, INFO, DEBUG

from news_parser.items import NewsItem

# scrapy crawl news_spider -a required_pages=2 (any integer)

class NewsSpider(scrapy.Spider):
    """Spider to parse forbes.ua site"""
    name = 'news_spider'
    allowed_domains = ["forbes.ua",]

    start_urls = ["http://forbes.ua/news"]

    def __init__(self, required_pages=1, *args, **kwargs):
        self.required_pages = required_pages
        super(NewsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        """Return request for every news_detail link.
        Create item instance, populate title field. 

        Test a sample response. Run 'scrapy check news_spider' to check.

        @url http://forbes.ua/news
        @returns request 20
        """
        try:
            current_index = response.meta['current_index']
        except KeyError:
            current_index= 1
        next_index = current_index + 1
        self.log('Next page index = %i' % next_index, INFO)
        # create url for next page
        next_page = "http://forbes.ua/news?p=%i" % next_index
        self.log('Next wisited page %s' % next_page, DEBUG)
        # stop parsing after required number of pages
        if next_index <= self.required_pages:
            # recursive call parse method for the paginated page
            yield scrapy.Request(next_page, self.parse,
                                 meta={'current_index':current_index})

        links = response.xpath('//div[@class="oh"]/h2/a')
        # only the links contained world 'news' will be remaining
        news_links = [link for link in links if 'news' in link.extract()]
        for link in news_links:
            detail_url = link.xpath('./@href').extract()[0]
            title = link.xpath('./text()').extract()[0]
            item = NewsItem()
            item['title'] = title
            yield scrapy.Request(detail_url, self.parse_detail,
                                 meta={'item':item})

    def parse_detail(self, response):
        """Parse page and populate item with body, img_url.

        @url http://forbes.ua/news
        @returns items 0 20
        """
        item = response.meta.get('item')
        if item:
            body = response.xpath('//div[@class="text_box"]/p/text()').extract()
            img_url = response.xpath('//div[@class="img_box1"]/img/@src').extract()
            item['image_urls'] = img_url
            item['body'] = body[0] # only first <p> will be recorded
            yield item
        else:
            self.log('No item instance was found in response.meta',
                      ERROR)


