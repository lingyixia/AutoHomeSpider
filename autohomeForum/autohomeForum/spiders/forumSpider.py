# -*- coding: utf-8 -*-
import scrapy, time, json, random, logging, re, requests, pymongo
from scrapy_splash import SplashRequest
from scrapy import Selector
from autohomeForum.items import AutohomeforumItem
from autohomeForum.ImageRecognize import ImageRecognizer
from scrapy.conf import settings


class ForumspiderSpider(scrapy.Spider):
    name = 'forumSpider'
    proxyMeta = "http://{proxyUser}:{proxyPass}@{proxyHost}:{proxyPort}".format(
        proxyUser=settings['PROXY_USER'],
        proxyPass=settings['PROXY_PASS'],
        proxyHost=settings['PROXY_HOST'],
        proxyPort=settings['PROXY_PORT'])
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    allowed_domains = ['club.autohome.com.cn']
    baseUrl = 'https://club.autohome.com.cn'
    start_urls = ['https://club.autohome.com.cn/bbs/forum-c-66-1.html#pvareaid=6825482',
                  'https://club.autohome.com.cn/bbs/forum-c-587-1.html#pvareaid=6825482',
                  'https://club.autohome.com.cn/bbs/forum-c-2968-1.html#pvareaid=6825482']
    pages = [10, 5, 5]

    url_pages = dict(zip(start_urls, pages))

    def start_requests(self):
        for url, page in self.url_pages.items():
            yield SplashRequest(url=url, callback=self.title_parse, args={'wait': 1, 'timeout': 60, 'images': 0},
                                meta={'page': page})

    def title_parse(self, response):
        selector = Selector(response)
        itemList = selector.xpath(
            "//div[@id = 'subcontent']/dl[contains(@class,'list_dl') and not(contains(@class,'bluebg'))]")
        for item in itemList:
            try:
                autohomeforumItem = AutohomeforumItem()
                autohomeforumItem['carId'] = re.findall('-(\d+)-', response.url)[0]
                autohomeforumItem['iconName'] = item.xpath("./dt/span/@class").extract_first()
                autohomeforumItem['title'] = item.xpath("./dt/a[1]/text()").extract_first()
                autohomeforumItem['author'] = item.xpath("./dd[1]/a/text()").extract_first()
                autohomeforumItem['authorId'] = item.xpath("./dd[1]/a/@href").extract_first().split('/')[-1]
                autohomeforumItem['publishTime'] = item.xpath("./dd[1]/span/text()").extract_first()
                autohomeforumItem['replyNum'] = item.xpath("./dd[2]/span[1]/text()").extract_first()
                autohomeforumItem['clickNum'] = item.xpath("./dd[2]/span[2]/text()").extract_first()
                autohomeforumItem['lastReplyer'] = item.xpath("./dd[3]/a/text()").extract_first()
                autohomeforumItem['lastReplyTime'] = item.xpath("./dd[3]/span/text()").extract_first()
                detialUrl = item.xpath("./dt/a[1]/@href").extract_first()
                autohomeforumItem['itemId'] = re.findall('/(\d+)-', detialUrl)[0]
                autohomeforumItem['url'] = self.baseUrl + detialUrl
                autohomeforumItem['contents'] = list()
                if self.isSavedInMongodb(
                        {'carId': autohomeforumItem['carId'], 'itemId': autohomeforumItem['itemId']}) > 0:
                    logging.warning(
                        '{carId}的{itemId}已经保存'.format(carId=autohomeforumItem['carId'],
                                                      itemId=autohomeforumItem['itemId']))
                    continue
                yield SplashRequest(url=self.baseUrl + detialUrl,
                                    callback=self.detial_parse,
                                    args={'wait': 1, 'timeout': 60, 'images': 0},
                                    meta={'autohomeforumItem': autohomeforumItem})
            except Exception as e:
                print(e)
        maxNumText = selector.xpath("//span[@class='fr']/text()").extract_first()
        try:
            maxNum = re.findall("(\d+)", maxNumText)[0]
        except Exception as e:
            print(e)
        currentPageNum = selector.xpath("//span[@class='cur']/text()").extract_first()
        if int(currentPageNum) < response.meta['page']:
            nextUrl = re.sub('\d+.html', str(int(currentPageNum) + 1) + '.html', response.url)
            yield SplashRequest(url=nextUrl, callback=self.title_parse,
                                args={'wait': 1, 'timeout': 60, 'images': 0}, meta=response.meta)

    def detial_parse(self, response):
        autohomeforumItem = response.meta['autohomeforumItem']
        selector = Selector(response)
        mainBody = selector.xpath("//div[@id='cont_main']")
        main_topic = mainBody.xpath("./div[@id='maxwrap-maintopic']")
        detailContent = autohomeforumItem['contents']
        topic_text = main_topic.xpath(".//div[contains(@class,'conttxt')]")
        topic_text = topic_text.xpath("string(.)").extract_first()
        # 检查是否有ttf
        cmp = re.compile(",url\('(//.*.ttf)'\) format\('woff'\)")
        rst = cmp.findall(response.body.decode('utf-8'))
        if rst:
            self.loopGet(self.savefont, rst[0])
        currentPage = int(re.findall('-(\d+)\.html', response.url)[0])
        if currentPage == 1:
            imageRecognizer = ImageRecognizer(orignText=topic_text, orignFont='temp.ttf')
            try:
                topic_text = ' '.join(imageRecognizer.outterCall().replace('\n', '').split())
                detailContent.append([' '.join(topic_text.replace('\n', '').split()), '楼主'])
            except Exception as e:
                print(e)
        main_replyList = mainBody.xpath("./div[@id='maxwrap-reply']/div")
        for replyItem in main_replyList:
            try:
                tempList = dict()
                floor = replyItem.xpath(".//button/text()").extract_first()
                authorId = replyItem.xpath(".//a[@xname='uname']/@href").extract_first().split('/')[-2]
                authorName = replyItem.xpath(".//a[@xname='uname']/text()").extract_first().strip()
                replyWho = replyItem.xpath(".//div[@class='relyhfcon']//a[2]/text()")
                publistTime = replyItem.xpath(".//span[@xname='date']/text()").extract_first()
                tempList['publishTime'] = publistTime
                if replyWho:  # 如果是回复某楼层的，则tempList第一个是内容，第二个是楼层
                    thisContent = replyItem.xpath(".//div[@class = 'yy_reply_cont']")
                    thisContent = thisContent.xpath("string(.)").extract_first()
                    if rst:
                        try:
                            imageRecognizer = ImageRecognizer(orignText=thisContent, orignFont='temp.ttf')
                            thisContent = ' '.join(imageRecognizer.outterCall().replace('\n', '').split())
                            tempList['thisContent'] = ' '.join(thisContent.replace('\n', '').split())
                            tempList['replyWho'] = ' '.join(replyWho.extract_first().replace('\n', '').split())
                        except Exception as e:
                            print(e)
                else:
                    thisContent = replyItem.xpath(".//div[contains(@class,'x-reply')]")
                    thisContent = thisContent.xpath("string(.)").extract_first()
                    if rst:
                        try:
                            imageRecognizer = ImageRecognizer(orignText=thisContent, orignFont='temp.ttf')
                            thisContent = ' '.join(imageRecognizer.outterCall().replace('\n', '').split())
                            tempList['thisContent'] = ' '.join(thisContent.replace('\n', '').split())
                            tempList['replyWho'] = '楼主'
                        except Exception as e:
                            print(e)
                tempList['floor'] = floor
                tempList['authorId'] = authorId
                tempList['authorName'] = authorName
                detailContent.append(tempList)
            except Exception as e:
                print(e)
        autohomeforumItem['scrapyTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        autohomeforumItem['contents'] = detailContent
        nextPageUrl = selector.xpath("//a[text()='下一页']/@href").extract_first()
        if nextPageUrl is not None:
            yield SplashRequest(url=self.baseUrl + nextPageUrl, callback=self.detial_parse,
                                args={'wait': 1, 'timeout': 60, 'images': 0},
                                meta={'autohomeforumItem': autohomeforumItem})
        else:
            yield autohomeforumItem

    # 暂存字体函数
    def savefont(self, response):
        # ttf = requests.get("http:" + response[0], stream=True)
        # with open('temp.ttf', "wb") as pdf:
        #     for chunk in ttf.iter_content(chunk_size=1024):
        #         if chunk:
        #             pdf.write(chunk)
        time.sleep(0.2)
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        cmp = re.compile("url\('(//.*.ttf)'\) format\('woff'\)")
        ttf = s.get("http:" + response[0], proxies=self.proxies, stream=True)
        if ttf.status_code != 200:
            raise RuntimeError('to many requests')
        with open('temp.ttf', "wb") as pdf:
            for chunk in ttf.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)

    # 循环执行某个函数
    def loopGet(self, fun, *args):
        downLim = 5
        topLim = 35
        num = 10
        while num:
            try:
                time.sleep(random.randint(1, 5))
                return fun(args)
            except Exception as e:
                logging.warning(e)
            downLim += 5
            topLim += 5
            num -= 1

    def isSavedInMongodb(self, argsDic):
        try:
            host = settings['MONGODB_HOST']
            port = settings['MONGODB_PORT']
            dbName = settings['MONGODB_DBNAME']
            client = pymongo.MongoClient(host=host, port=port)
            tdb = client[dbName]
            post = tdb[settings['MONGODB_DOCNAME']]
            datas = post.find(argsDic)
            datas.close()
            client.close()
            return datas.count()
        except Exception as e:
            logging.warning(e)
