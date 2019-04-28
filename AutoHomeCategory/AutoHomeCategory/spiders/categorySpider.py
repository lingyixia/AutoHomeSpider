# -*- coding: utf-8 -*-
import scrapy, json, time, re, logging, pymysql, pymongo
from scrapy import Selector
from AutoHomeCategory.items import AutohomecategoryItem
import AutoHomeCategory.settings as settings


class CategoryspiderSpider(scrapy.Spider):
    name = 'categorySpider'
    baseUrl = 'https://k.autohome.com.cn'
    start_urls = []

    def start_requests(self):
        db = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                             password=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME,
                             port=settings.MYSQL_PORT)
        cursor = db.cursor()
        cursor.execute('SELECT * FROM specificids where id>661 and id<=800')
        rows = cursor.fetchall()
        for row in rows:
            for item in json.loads(row[2]):
                self.start_urls.append(self.baseUrl + '/spec/' + str(item['SpecId']) + '/')
        cursor.close()
        db.close()
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.judge_parse, meta={'dont_redirect': True})

    def judge_parse(self, response):
        selector = Selector(response)
        allCategory = {'最满意': 'ge10/?=g#dataList', '最不满意': 'ge11/?=g#dataList', '空间': 'ge4/?=g#dataList',
                       '动力': 'ge5/?=g#dataList', '操控': 'ge6/?=g#dataList', '油耗': 'ge7/?=g#dataList',
                       '舒适性': 'ge3/?=g#dataList', '外观': 'ge1/?=g#dataList', '内饰': 'ge2/?=g#dataList',
                       '性价比': 'ge8/?=g#dataList'}
        allTags = selector.xpath("//div[@class='revision-impress ']/a")
        if len(allTags) > 0:
            for key, value in allCategory.items():
                yield scrapy.Request(url=response.url + value, dont_filter=True, callback=self.tag_parse,
                                     meta={'category': key, 'dont_redirect': True})

    def tag_parse(self, response):
        selector = Selector(response)
        specId = re.findall('spec/(\d+)', response.url)[0]
        contentPageNum = \
            re.findall(('\d+'), selector.xpath("//div[contains(@class,'tab-nav')]/span/text()").extract_first())[0]
        if contentPageNum == '0':
            logging.info('{specId}没有评论'.format(specId=specId))

        allTags = selector.xpath("//div[@class='revision-impress ']/a")[1:]
        for tag in allTags:
            tagName = tag.xpath("./text()").extract_first()
            url = self.baseUrl + tag.xpath("./@href").extract_first()
            response.meta['tagName'] = tagName
            response.meta['specId'] = specId
            if tag.xpath('./@class').extract_first() == ' ':
                response.meta['actOrNeg'] = True
            else:
                response.meta['actOrNeg'] = False
            yield scrapy.Request(url=url, callback=self.content_parse, meta=response.meta)

    def content_parse(self, response):
        selector = Selector(response)
        contentPageNum = \
            re.findall(('\d+'), selector.xpath("//div[contains(@class,'tab-nav')]/span/text()").extract_first())[0]
        savedNum = self.isSavedInMongodb(
            {'specId': response.meta['specId'], 'category': response.meta['category'], 'tag': response.meta['tagName']})
        if abs(int(contentPageNum) - savedNum) <= int(contentPageNum) // 10:
            logging.info(
                '{specId}已保存{saved},一共有{all},评论基本已经抓完'.format(specId=response.meta['specId'], saved=savedNum,
                                                              all=int(contentPageNum)))
            return
        autohomecategoryItem = AutohomecategoryItem()
        allItems = selector.xpath("//div[@class='mouth-main mouth-min-main']")
        modelId = selector.xpath("//div[@class='text-right']/a/@href").extract_first().split('/')[1]
        for item in allItems:
            commentsId = item.xpath("./div[@class='nav-sub']//a[@data-val]/@data-val").extract_first()
            noTagedContents = ''.join(item.xpath("./div[@class='mouth-item']/div[@class='text-con']").xpath(
                './text()|./font/text()').extract())
            tagedContents = item.xpath("./div[@class='mouth-item']/div[@class='text-con']/font/text()").extract()
            tempDic = dict()
            tempDic['commentsId'] = commentsId
            tempDic['noTagedContents'] = noTagedContents
            tempDic['tagedContents'] = tagedContents
            # contents.append(tempDic)
            autohomecategoryItem['scrapyTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            autohomecategoryItem['specId'] = response.meta['specId']
            autohomecategoryItem['contents'] = tempDic
            autohomecategoryItem['category'] = response.meta['category']
            autohomecategoryItem['tag'] = response.meta['tagName']
            autohomecategoryItem['actOrNeg'] = response.meta['actOrNeg']
            autohomecategoryItem['modelId'] = modelId
            savedNum = self.isSavedInMongodb(
                {'specId': response.meta['specId'], 'category': response.meta['category'],
                 'tag': response.meta['tagName'], 'contents.commentsId': commentsId})
            if savedNum > 0:
                logging.info(str({'specId': response.meta['specId'], 'category': response.meta['category'],
                                  'tag': response.meta['tagName'], 'contents.commentsId': commentsId}) + '已经保存')
                continue
            yield autohomecategoryItem
        nextPageUrl = selector.xpath("//a[@class='page-item-next']/@href").extract_first()
        if nextPageUrl:
            yield scrapy.Request(url=self.baseUrl + nextPageUrl, callback=self.content_parse, meta=response.meta)

    # 读取mongodb，判断是否已经爬过该commentsId的页面
    def isSavedInMongodb(self, argsDic):
        host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        dbName = settings.MONGODB_DBNAME
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        post = tdb[settings.MONGODB_DOCNAME]
        datas = post.find(argsDic)
        datas.close()
        client.close()
        return datas.count()
        # mailer = MailSender.from_settings(settings)
        # mailer.send('chinachenfeiyu@outlook.com', 'scrapy', (e + 'Mongo异常').encode('utf-8'), charset='utf-8')
