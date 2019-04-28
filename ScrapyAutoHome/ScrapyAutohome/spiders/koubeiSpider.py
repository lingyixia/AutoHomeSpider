# -*- coding: utf-8 -*-
from scrapy.conf import settings
import re, json, requests, time, scrapy, math, logging, random, pymongo, pymysql, os
from scrapy import Selector
from scrapy_splash import SplashRequest
from ScrapyAutohome.items import EntireContentsItem
from ScrapyAutohome.ImageRecognize import ImageRecognizer
from scrapy.mail import MailSender


class KoubeispiderSpider(scrapy.Spider):
    name = 'koubeiSpider'
    proxyMeta = "http://{proxyUser}:{proxyPass}@{proxyHost}:{proxyPort}".format(
        proxyUser=settings['PROXY_USER'],
        proxyPass=settings['PROXY_PASS'],
        proxyHost=settings['PROXY_HOST'],
        proxyPort=settings['PROXY_PORT'])
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    # allowed_domains = ['k.autohome.com.cn']
    baseUrl = 'https://k.autohome.com.cn/spec/'
    start_urls = []  # 测试

    # def start_requests(self):
    #     self.start_urls.append('https://k.autohome.com.cn/spec/32040')
    #     for url in self.start_urls:
    #         yield SplashRequest(url=url, callback=self.specHome_parse, endpoint='render.html',
    #                             args={'wait': 5, 'timeout': 60, 'images': 0})

    def start_requests(self):
        db = pymysql.connect(host=settings['MYSQL_HOST'], user=settings['MYSQL_USER'],
                             password=settings['MYSQL_PASSWD'], db=settings['MYSQL_DBNAME'],
                             port=settings['MYSQL_PORT'])
        cursor = db.cursor()
        # <=2000
        cursor.execute('SELECT * FROM specificids where id>=2500 and id<3000')
        rows = cursor.fetchall()
        for row in rows:
            for item in json.loads(row[2]):
                self.start_urls.append(self.baseUrl + str(item['SpecId']))
        cursor.close()
        db.close()
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.specHome_parse, args={'wait': 5, 'timeout': 60, 'images': 0})

    def testip_parse(self, response):
        selector = Selector(response)
        ip = selector.xpath('//tr[3]//td/text()').extract_first()
        print(ip)

    def specHome_parse(self, response):
        # yield SplashRequest(url='http://test.abuyun.com/', callback=self.testip_parse, dont_filter=True)
        selector = scrapy.Selector(response)
        specId = re.findall('spec/(\d+)', response.url)[0]
        try:
            contentPageNum = \
                re.findall(('\d+'), selector.xpath("//div[contains(@class,'tab-nav')]/span/text()").extract_first())[0]
        except Exception as e:
            print(e)
            return
        firstPage = re.findall('index_(\d+).html', response.url)
        if len(firstPage) == 0 or int(firstPage[0]) == 1:
            savedNum = self.isSavedInMongodb({'specId': specId})
            if contentPageNum == '0':
                if savedNum > 0:
                    logging.info('{specId}没有评论,已经保存占位项，不用在保存了'.format(specId=specId))
                    return
                else:
                    entireContentsItem = EntireContentsItem()
                    entireContentsItem['specId'] = specId
                    logging.info('{specId}没有评论,保存一个占位项'.format(specId=specId))
                    yield entireContentsItem
            elif abs(int(contentPageNum) - savedNum) <= int(contentPageNum) // 10:
                # print(specId,'评论基本已经抓完')
                logging.info(
                    '{specId}已保存{saved},一共有{all},评论基本已经抓完'.format(specId=specId, saved=savedNum,
                                                                  all=int(contentPageNum)))
                return
        leftBarAndContents = selector.xpath("//div[@class='mouthcon']")
        for leftBarAndContent in leftBarAndContents:
            content = leftBarAndContent.xpath('./div/div')[1]
            commentsId = content.xpath(".//a[@data-val]/@data-val").extract_first()
            if self.isSavedInMongodb({'commentsId': commentsId}) > 0:
                continue
            allContentUrl = content.xpath('.//a[contains(text(),"查看全部内容")]/@href').extract_first()
            leftBar = leftBarAndContent.xpath("./div/div")[0]
            userName = leftBar.xpath(".//div[@class='name-text']//a/text()").extract_first()  # 评论用户名
            userId = leftBar.xpath(".//div[@class='name-text']//a/@href").extract_first().split('/')[-1]
            names = [i.xpath('string(.)').extract_first().replace(' ', '').replace('\n', '') for i in
                     leftBar.xpath(".//dl[contains(@class,'choose-dl')]/dt")]
            names = [i for i in names if i is not '']
            values = [i.xpath('string(.)').extract_first().replace(' ', '').replace('\n', '') for i in
                      leftBar.xpath(".//dl[contains(@class,'choose-dl')]/dd")]
            values = [i for i in values if i is not '']
            nameValueDic = dict(zip(names, values))
            nameValueDic['username'] = userName.replace('\n', '').replace(' ', '')
            nameValueDic['userId'] = userId
            try:
                yield SplashRequest(url='http:' + allContentUrl, callback=self.content_parse,
                                    args={'wait': 5, 'timeout': 60, 'images': 0},
                                    meta={'specId': specId, 'commentsId': commentsId, 'nameValueDic': nameValueDic})
            except Exception as e:
                print(e)
        nextPageUrl = selector.xpath("//a[@class='page-item-next']/@href").extract_first()
        if nextPageUrl:
            yield SplashRequest(url='https://k.autohome.com.cn' + nextPageUrl, callback=self.specHome_parse,
                                args={'wait': 5, 'timeout': 60, 'images': 0})

    def content_parse(self, response):
        selector = Selector(response=response)

        self.loopGet(self.savefont, response)
        contents = selector.xpath("//div[contains(@class,'koubei-final')]")[0]
        publishTime = contents.xpath(".//div[contains(@class,'title-name')]/b/text()").extract_first()
        publishTitle = contents.xpath(".//div[contains(@class,'kou-tit')]//text()").extract()
        publishTitle = ''.join(publishTitle)
        publishTitle = publishTitle.strip('\n').strip('\t').strip()
        contentsText = contents.xpath(
            ".//div[contains(@class,'text-con')]/text()|.//div[contains(@class,'text-con')]//span/text()").extract()
        contentsText = ''.join(contentsText)
        contentsText = contentsText.strip('\n').strip('\t').strip()
        contentsDic = dict()
        contentsDic['publishTime'] = publishTime
        contentsDic['publishTitle'] = publishTitle
        imageRecognizer = ImageRecognizer(orignText=contentsText, orignFont='temp.ttf')
        contentsDic['contentsText'] = ' '.join(imageRecognizer.outterCall().replace('\n', '').split())
        entireContentsItem = EntireContentsItem()
        entireContentsItem['url'] = response.url
        entireContentsItem['specId'] = response.meta['specId']
        entireContentsItem['commentsId'] = response.meta['commentsId']
        entireContentsItem['leftBar'] = response.meta['nameValueDic']
        ifRenzhen = selector.xpath("//i[@class='renzhen']").extract_first()
        if ifRenzhen:
            entireContentsItem['leftBar']['renzhen'] = True
        else:
            entireContentsItem['leftBar']['renzhen'] = False
        modelId = selector.xpath("//dl[@class='choose-dl'][1]//a[1]/@href").extract_first().replace('/', '')
        entireContentsItem['modelId'] = modelId
        entireContentsItem['contents'] = contentsDic
        allCommentsNum = selector.xpath('//span[@id="Comment_{commentsId}"]//text()'.format(
            commentsId=entireContentsItem['commentsId'])).extract_first()
        if allCommentsNum is None:
            with open('temp.txt', 'rb') as writer:
                writer.write(response)
            mailer = MailSender.from_settings(settings)
            mailer.send('chinachenfeiyu@outlook.com', 'scrapy', 'allCommentsNum is None'.encode('utf-8'),
                        charset='utf-8')
        try:
            allPagesNum = math.ceil(int(allCommentsNum) / 10)
        except Exception as e:
            logging.warning(e)
        #entireContentsItem['comments'] = self.getComments(entireContentsItem['commentsId'], allPagesNum)
        entireContentsItem['comments']=list()
        entireContentsItem['scrapyTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield entireContentsItem

    # 暂存字体函数
    def savefont(self, response):
        time.sleep(0.2)
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        cmp = re.compile("url\('(//.*.ttf)'\) format\('woff'\)")
        rst = cmp.findall(response[0].body.decode('utf-8'))
        ttf = s.get("http:" + rst[0], proxies=self.proxies, stream=True)
        if ttf.status_code != 200:
            raise RuntimeError('to many requests')
        with open('temp.ttf', "wb") as pdf:
            for chunk in ttf.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
        return

    # 单页评论抓取，为了方便循环，单独拿出来
    def getSingleComments(self, url):
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        try:
            time.sleep(0.2)
            contents = s.get(url=url, proxies=self.proxies).text
            contentsJson = json.loads(contents)['commentlist']
        except Exception as e:
            logging.warning(e)
            return ''
        return contentsJson

    # 保存评论信息
    def getComments(self, commentsId, allPagesNum):
        allComments = list()
        currentPage = allPagesNum
        while currentPage:
            url = "https://reply.autohome.com.cn/ShowReply/ReplyJsonredis.ashx?&page={currentPage}&id={commentsId}&appid=5".format(
                currentPage=currentPage, commentsId=commentsId)
            allComments += self.getSingleComments(url)
            currentPage -= 1
        return allComments

    # 循环执行某个函数
    def loopGet(self, fun, *args):
        downLim = 5
        topLim = 35
        num = 10
        while num:
            try:
                time.sleep(random.randint(0,2))
                return fun(args)
            except Exception as e:
                logging.warning(e)
            downLim += 5
            topLim += 5
            num -= 1

    # 读取mongodb，判断是否已经爬过该commentsId的页面
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
            mailer = MailSender.from_settings(settings)
            mailer.send('chinachenfeiyu@outlook.com', 'scrapy', (e + 'Mongo异常').encode('utf-8'), charset='utf-8')

    # ------------------------------------------------depreced-------------------------------------------------------
    # 先不用他了
    def comments_parse(self, response):
        selector = Selector(response)
        pageNum = int(re.findall('page=(\d+)&', response.url)[0])
        if pageNum > 0:
            if '<html>' in response.text:
                contentsJson = json.loads(selector.xpath('//pre/text()').extract_first())['commentlist']
            else:
                contentsJson = json.loads(response.text)['commentlist']
            response.meta['entireContentsItem']['comments'] += contentsJson
            pageNum -= 1
            url = re.sub('page=(\d+)&', 'page={pageNum}&'.format(pageNum=pageNum), response.url)
            yield SplashRequest(url=url, callback=self.comments_parse, meta=response.meta)
        else:
            entireContentsItem = response.meta['entireContentsItem']
            yield entireContentsItem
        script = """
                function main(splash, args)
                  splash.images_enabled = false
                  splash.plugins_enabled=false
                  splash.resource_timeout=30
                  assert(splash:wait(args.wait))
                  assert(splash:go{
                  splash.args.url,
                  headers=splash.args.headers,
                  http_method=splash.args.http_method,
                  body=splash.args.body,
                  })
                  return splash:html()
                end
                """
