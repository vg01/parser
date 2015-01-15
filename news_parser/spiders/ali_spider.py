import urllib
import scrapy
import scrapy.log

from scrapy.http import Request
from scrapy.log import ERROR, WARNING, INFO, DEBUG

from news_parser.items import AliItem


# scrapy crawl ali_spider -a search_term='...' (str)
class AliSpider(scrapy.Spider):
    """Spider to parse aliexpress.com"""
    name = 'ali_spider'
    allowed_domains = ['aliexpress.com']

    SEARCH_URL = "http://www.aliexpress.com/premium/{search_term}.html?ltype" \
                 "=wholesale&SearchText={search_term}"

    def __init__(self, search_term='', required_pages=2, *args, **kwargs):
        super(AliSpider, self).__init__(*args, **kwargs)
        self.search_term = urllib.quote_plus(search_term.strip())
        self.required_pages = required_pages

    def start_requests(self):
        """Create requests for search url formated with search term.
        Add search term to request.meta
        """
        yield Request(self.SEARCH_URL.format(search_term=self.search_term),
                      meta={'search_term': self.search_term})

    def make_requests_from_url(self, url):
        """This method fully replaced by start_requests method"""
        raise AssertionError("Need a search term.")

    def parse(self, response):
        """Parse page, find detail links for all item, return response
        prepopulated with item instance and additional meta data.
        Also find link to the next page and call function recursively.
        """
        self.log('Parsing url %s' % response.url, INFO)
        search_term = response.meta.get('search_term')

        # found link for next page
        # not performed yet
        current_page = response.meta.get('current_page')
        next_page = response.meta.get('next_page')
        if not current_page and not next_page:
            current_page = 1
            next_page = 2
        else:
            current_page += 1
            next_page += 1
        # define initial meta data that will be used with responses
        meta = {'current_page': current_page,
                'next_page': next_page,
                'search_term': search_term}

        if next_page <= self.required_pages:
            try:
                self.log('Commenced parse page number %s' % next_page, INFO)
                next_link = response.xpath(
                    '//a[@class="page-next"]/@href'
                    ).extract()[0]
                yield Request(next_link, self.parse, meta=meta)
            # next_link is blank, no next page was found
            except IndexError:
                self.log('No next page was found', ERROR)

        # find links for product details
        links = response.xpath(
            '//li[contains(@class,"list-item")]//a[contains\
            (@class, "history-item product")]/@href'
            ).extract()
        if links:
            products_per_page = len(links)
            i = 1
            for link in links:
                search_rank = i + products_per_page*(current_page - 1)
                i += 1
                item = AliItem()
                item['search_rank'] = search_rank
                item['link'] = link
                total_matches = response.xpath(
                    '//strong[@class="search-count"]/text()').extract()
                item['total_matches'] = total_matches[0].replace(',', '')
                item['products_per_page'] = products_per_page
                # add item instance to meta dictionary
                meta['item'] = item
                yield Request(link, self.parse_detail, meta=meta)
        # handle if no any links were found.
        else:
            fail_string = "Please try again"
            fail_answer = response.xpath(
                '//div[contains(@class, "board-attention")]/text()'
            ).extract()
            if fail_answer:
                if fail_string in fail_answer[1]:
                    self.log('Nothng was found with search_term %s'
                             % search_term, ERROR)

    def parse_detail(self, response):
        """Parse page and populate item with required info"""
        item = response.meta.get('item')
        current_page = response.meta.get('current_page')
        next_page = response.meta.get('next_page')
        if not item:
            self.log('Item was not populated', ERROR)

        # create dictionary of meta properties and contents
        metadata_dom = response.xpath("/html/head/meta[@property]")
        props = metadata_dom.xpath("@property").extract()
        conts = metadata_dom.xpath("@content").extract()

        meta_dict = {p: c for p, c in zip(props, conts)}

        search_term = response.meta.get('search_term')
        item['search_term'] = search_term
        item['page_number'] = current_page

        try:
            # asume price set in one number format
            price = response.xpath(
                '//span[@itemprop="price"]/text()'
            ).extract()
            price_str = price[0]
        except IndexError:
            # price set inf format low-high
            price_low = response.xpath(
                '//span[@itemprop="lowPrice"]/text()'
            ).extract()
            price_high = response.xpath(
                '//span[@itemprop="highPrice"]/text()'
            ) .extract()
            price_str = "{low}-{high}".format(low=price_low[0],
                                              high=price_high[0])
        item['price'] = "USD {price}".format(price=price_str)

        # title with stiped ' on Aliexpress.com | Alibaba Group'
        info_string = ' Aliexpress.com | Alibaba Group'
        # was made spited cause in case use whole word also sh'oes striped
        string_on = ' on'
        item['title'] = meta_dict.get('og:title').\
            rstrip(info_string).rstrip(string_on)
        yield item
