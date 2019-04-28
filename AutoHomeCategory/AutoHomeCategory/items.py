# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutohomecategoryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    scrapyTime = scrapy.Field()
    specId = scrapy.Field()
    category = scrapy.Field()
    tag = scrapy.Field()
    contents = scrapy.Field()
    commentsId = scrapy.Field()
    actOrNeg = scrapy.Field()  # 1代表active 0代表negative
    modelId=scrapy.Field()
