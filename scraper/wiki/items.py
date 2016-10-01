# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WikiItem(scrapy.Item):
    # define the fields for your item here like:
    comment = scrapy.Field()
    date = scrapy.Field()
    ip = scrapy.Field()
    user = scrapy.Field()
    size = scrapy.Field()
    tags = scrapy.Field()
