# -*- coding: utf-8 -*-

# Scrapy settings for news_parser project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'news_parser'

SPIDER_MODULES = ['news_parser.spiders']
NEWSPIDER_MODULE = 'news_parser.spiders'

DOWNLOAD_DELAY = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'news_parser (+http://www.yourdomain.com)'
