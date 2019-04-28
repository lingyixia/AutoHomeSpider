from bs4 import BeautifulSoup
import os, re, csv


class LefaBarr:
    def __init__(self, modelIdDic, sourcePath, savePath):
        self.modelIdDic = modelIdDic
        self.sourcePath = sourcePath
        self.savePath = savePath

    def parserComment(self,textFile, listData):
        comment = ''
        with open(textFile, 'rb') as reader:
            comment = reader.read()
        comment = comment.decode('utf-8', errors='ignore').replace(' ', '')
        labels = re.findall('】(.*?)【', comment)
        for label in labels:
            listData.append(label)
        print('{file}处理完毕'.format(file=textFile))
        return listData

    def parseLeftBar(self,htmlFile):
        print('正在处理{htmlFile}'.format(htmlFile=htmlFile))
        listData = []
        soup = BeautifulSoup(open(htmlFile, 'rb'), 'html.parser')
        try:
            ahref_UserId = soup.find('div', class_='user-name').find('a', id='ahref_UserId').text.replace(' ', '')
        except Exception:
            pass
        authoried = soup.find('div', class_='user-info').find('i', class_='renzhen')
        if authoried:
            authoried = '是'
        else:
            authoried = '否'
        leftBarList = soup.find('div', class_='mouthcon-cont-left').find('div', class_='choose-con').findAll('dl',
                                                                                                             class_='choose-dl')
        for node in leftBarList:
            if '购买车型' in node.find('dt').text:
                modelName = node.find('dd').findAll('a')[0].text.replace(' ', '')
                modelNameDetial = node.find('dd').findAll('a')[1].text.replace(' ', '')
            elif '购买时间' in node.find('dt').text:
                time = node.find('dd').text.replace(' ', '')
            elif '购买地点' in node.find('dt').text:
                place = node.find('dd').text.replace(' ', '')
            elif '购车目的' in node.find('dt').text:
                destination = node.find('dd').text.replace('\n', '')
        listData.append('汽车之家口碑')
        listData.append(ahref_UserId.replace('\n', ''))
        listData.append(authoried.replace('\n', ''))
        listData.append(modelName.replace('\n', ''))
        listData.append(modelNameDetial.replace('\n', ''))
        listData.append(time.replace('\n', ''))
        listData.append(place.replace('\n', ''))
        listData.append(re.sub('\s+', ' ', destination))

        return listData

    def outterLeftbar(self):
        for entryId, modelIds in self.modelIdDic.items():
            listCsv = []
            for modelId in modelIds:
                basePath = os.path.join(self.sourcePath, str(entryId), str(modelId))
                allNum = len([i for i in os.listdir(basePath) if i.endswith('html')])
                for pageNum in range(1, allNum + 1):
                    listData = self.parseLeftBar(os.path.join(basePath, str(pageNum) + '.html'))
                    listData = self.parserComment(os.path.join(basePath, str(pageNum) + '.txt'), listData)  # 加入comments
                    listCsv.append(listData)
            with open(os.path.join(self.savePath, str(entryId) + '.csv'), 'w', newline='',
                      errors='ignore') as writer:
                writer = csv.writer(writer)
                writer.writerows(listCsv)

# if __name__ == '__main__':
#     modelIdNum = {}
#     for entryId, modelIds in modelIdDic.items():
#         listCsv = []
#         for modelId in modelIds:
#             basePath = os.path.join('prizePages', str(entryId), str(modelId))
#             for pageNum in range(1, int(len(os.listdir(basePath)) / 3 + 1)):
#                 listData = parseLeftBar(os.path.join(basePath, str(pageNum) + '.html'))
#                 listData = parserComment(os.path.join(basePath, str(pageNum) + '.txt'), listData)  # 加入comments
#                 listCsv.append(listData)
#         with open(os.path.join('export_koubei_article_multi', str(entryId) + '.csv'), 'w', newline='',
#                   errors='ignore') as writer:
#             writer = csv.writer(writer)
#             writer.writerows(listCsv)
