# -*- coding: utf-8 -*-

# Scrapy settings for news_parser project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os

BOT_NAME = 'news_parser'

SPIDER_MODULES = ['news_parser.spiders']
NEWSPIDER_MODULE = 'news_parser.spiders'

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
    'news_parser.pipelines.JsonWritePipeline': 100,
    }
# for image handling
base_directory = os.path.abspath(os.getcwd())
IMAGES_STORE = os.path.join(base_directory,'images')

# for Item Exports except pipeline
export_storage = os.path.join(base_directory, 'export.json')
FEED_URI = export_storage
FEED_FORMAT = 'json'
# FEED_STORAGES 
# FEED_EXPORTERS
# FEED_STORE_EMPTY


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'news_parser (+http://www.yourdomain.com)'
