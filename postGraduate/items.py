# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostgraduateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 研招网Item
class yanzhaowangItem(scrapy.Item):
    collection = table = 'yanzhaowang'
    Institution = scrapy.Field()
    location = scrapy.Field()
    subjection = scrapy.Field()
    is985 = scrapy.Field()
    is211 = scrapy.Field()
    haveGraduateSchool = scrapy.Field()
    isSelfMarkingSchool = scrapy.Field()
    url = scrapy.Field()

