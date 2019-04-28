# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutohomeforumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    iconName = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    publishTime = scrapy.Field()
    replyNum = scrapy.Field()
    clickNum = scrapy.Field()
    lastReplyer = scrapy.Field()
    lastReplyTime = scrapy.Field()
    contents = scrapy.Field()
    scrapyTime = scrapy.Field()
    carId = scrapy.Field()
    itemId = scrapy.Field()
    authorId = scrapy.Field()
    url = scrapy.Field()
