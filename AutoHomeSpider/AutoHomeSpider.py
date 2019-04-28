import time, requests, random, json, os, re
from bs4 import BeautifulSoup
from ImageRecognize import ImageRecognizer
from LeftBar import LefaBarr


class AutoHomePrizeSpider:
    def __init__(self, baseUrl, headers, modelIdDic, sourcePath, savePath):
        self.headers = headers
        self.baseUrl = baseUrl
        self.modelIdDic = modelIdDic
        self.sourcePath = sourcePath
        self.savePath = savePath

    # 直接获取完整评价页面的url，保存在urls/entryID.json中
    def getEntirePageUrl(self):
        for entryId, modelIds in self.modelIdDic.items():
            entireUrls = {}
            for modelId in modelIds:
                num = 0
                entireUrl = []
                ifHasNext = "hasNext"
                while ifHasNext:
                    num += 1
                    if num == 1:
                        href = '/spec/{modelid}'.format(baseurl=self.baseUrl, modelid=modelId)
                    else:
                        href = ifHasNext.get('href')
                    nextPageUrl = '{baseurl}{url}'.format(baseurl=self.baseUrl, url=href)
                    littleTime = 10
                    bigTime = 20
                    testNum = 1
                    while testNum <= 10:
                        try:
                            time.sleep(random.randint(littleTime, bigTime))
                            content = requests.get(url=nextPageUrl, headers=self.headers).content
                            soup = BeautifulSoup(content, 'html.parser')
                            entireDiv = soup.findAll('div', class_='allcont')
                            if len(entireDiv) > 0:
                                break
                            else:
                                testNum += 1
                                if testNum == 11:
                                    print('去你大爷的，老子不要了！！！')
                                    break
                                else:
                                    print('获取出错，正在进行第{testNum}次尝试'.format(testNum=testNum))
                                    littleTime += 10
                                    bigTime += 10
                        except Exception:
                            testNum += 1
                            if testNum == 11:
                                print('去你大爷的，老子不要了！！！')
                                break
                            else:
                                print('获取出错，正在进行第{testNum}次尝试'.format(testNum=testNum))
                                littleTime += 10
                                bigTime += 10

                    for url in entireDiv:
                        entireUrl.append('https:{url}'.format(url=url.find('a').get('href')))
                    print('%d第%d页地址收集完成,正在转下一页' % (modelId, num))
                    ifHasNext = soup.find('a', class_='page-item-next')
                    tag = soup.find('a', class_='page-disabled page-item-next')
                    if tag:
                        break
                print('没有下一页了{modelId}地址收集完成,正在转下一个车型'.format(modelId=modelId))
                entireUrls[modelId] = entireUrl
            with open(os.path.join('urls', str(entryId) + '.json'), 'w') as writer:
                json.dump(entireUrls, writer, ensure_ascii=False)

    # 读取urls/entryID.json，保存整体页面和字体
    def getModelEntirePrize(self, driver):
        for entryId, modelIds in self.modelIdDic.items():
            modelAndUrls = {}
            with open(os.path.join('urls', str(entryId) + '.json'), 'r') as reader:
                modelAndUrls = json.load(reader)
            for modelId in modelAndUrls:
                if int(modelId) not in modelIds:
                    continue
                num = 1
                path = os.path.join(self.sourcePath, str(entryId), str(modelId))
                if not os.path.exists(path):
                    os.makedirs(path)
                for url in modelAndUrls[modelId]:
                    if num!=66 and num!= 74:
                        num+=1
                        continue
                    littleTime = 10
                    bigTime = 20
                    testNum = 1
                    while testNum <= 10:
                        time.sleep(random.randint(littleTime, bigTime))
                        driver.get(url)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        cmp = re.compile("url\('(//.*.ttf)'\) format\('woff'\)")
                        rst = cmp.findall(soup.prettify())
                        try:
                            time.sleep(random.randint(littleTime, bigTime))
                            ttf = requests.get("http:" + rst[0], stream=True)
                            break
                        except Exception as e:
                            testNum += 1
                            if testNum == 11:
                                print('去你大爷，老子不要了')
                                break
                            print("获取字体失败，正在进行第{testNum}次尝试".format(testNum=testNum), e)
                            littleTime += 10
                            bigTime += 10
                    try:
                        with open(os.path.join(path, str(num) + '.ttf'), "wb") as pdf:
                            for chunk in ttf.iter_content(chunk_size=1024):
                                if chunk:
                                    pdf.write(chunk)
                            print('{modelId}第{num}个字体保存完毕'.format(modelId=modelId, num=num))
                    except Exception as e:
                        print(e)
                        print('{modelId}第{num}个字体保存失败'.format(modelId=modelId, num=num))
                    try:
                        with open(os.path.join(path, str(num) + '.html'), "wb") as page:
                            page.write(soup.prettify().encode('utf-8', errors='ignore'))
                            print('{modelId}第{num}个页面保存完毕'.format(modelId=modelId, num=num))
                    except Exception as e:
                        print(e)
                        print('{modelId}第{num}个页面保存失败'.format(modelId=modelId, num=num))
                    num += 1

    def imageRecognize(self):
        imgRecognizer = ImageRecognizer(modelIdDic=self.modelIdDic)
        imgRecognizer.outterCall(sourcePath=self.sourcePath)

    def leftBar(self):
        leftBarr = LefaBarr(self.modelIdDic, self.sourcePath, self.savePath)
        leftBarr.outterLeftbar()
