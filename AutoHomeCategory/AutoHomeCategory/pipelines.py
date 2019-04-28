# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo
import AutoHomeCategory.settings as settings

class AutohomecategoryPipeline(object):
    def __init__(self):
        host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        dbName = settings.MONGODB_DBNAME
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings.MONGODB_DOCNAME]

    def process_item(self, item, spider):
        entireContentsItem = dict(item)
        self.post.insert(entireContentsItem)
        return item

    # def close_spider(self, spider):
    #     mailer = MailSender.from_settings(settings)
    #     mailer.send('chinachenfeiyu@outlook.com', 'scrapy', '运行完毕'.encode('utf-8'), charset='utf-8')

