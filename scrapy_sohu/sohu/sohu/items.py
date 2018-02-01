# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SohuItem(scrapy.Item):
    Title = scrapy.Field()
    PublishTime = scrapy.Field()
    SourceType = scrapy.Field()
    Source = scrapy.Field()
    Content = scrapy.Field()
    Url = scrapy.Field()
    Author = scrapy.Field()
    Favorites = scrapy.Field()
    ReadCounts = scrapy.Field()
    Status = scrapy.Field()
    Category_ID = scrapy.Field()
    Source_ID = scrapy.Field()
    Keywords = scrapy.Field()
