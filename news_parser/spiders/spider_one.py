import scrapy
from news_parser.items import NewsItem

class NewsSpider(scrapy.Spider):
    name = 'news_spider'
    allowed_domains = ["forbes.ua",]

    start_urls = ["http://forbes.ua/news"]

    required_pages = 3

    def parse(self, response):
        try:
            current_index = response.meta['current_index']
        except KeyError:
            current_index= 1
        next_index = current_index + 1
        # create url for next page
        next_page = "http://forbes.ua/news?p=%i" % next_index
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
        item = response.meta['item']
        body = response.xpath('//div[@class="text_box"]/p/text()').extract()
        item['body'] = body[0] # only first <p> will be recorded
        yield item


