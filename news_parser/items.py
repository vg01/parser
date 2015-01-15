# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    """Item for forbes.ua"""
    title = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()
    # feilds for image parsing
    image_urls = scrapy.Field()
    images = scrapy.Field()


class AliItem(scrapy.Item):
    """Item for aliexpress.com"""
    title = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    search_term = scrapy.Field()
    page_number = scrapy.Field()
    total_matches = scrapy.Field()
    products_per_page = scrapy.Field()
    search_rank = scrapy.Field()
