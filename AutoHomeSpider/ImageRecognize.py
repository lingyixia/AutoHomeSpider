from fontTools.ttLib import TTFont
from PIL import Image, ImageFont, ImageDraw
import numpy as np
from bs4 import BeautifulSoup
import os, re


# 获取模板字符集中的对应关系，只需运行一次即可
class ImageRecognizer:
    def __init__(self, modelIdDic):
        self.modelIdDic = modelIdDic

    def getTemplateFont(self):
        templateDic = {}
        font = TTFont('template.TTF')
        uniList = font['cmap'].tables[0].ttFont.getGlyphOrder()
        arr = [eval("u'\\\\u" + uni[3:] + "'") for uni in uniList[1:]]

        arr = list(set(arr))
        for value in arr:
            try:
                text = bytes(value, 'ascii').decode('unicode_escape')
            except Exception as e:
                pass
            img = Image.new('1', (50, 50), 1)
            dr = ImageDraw.Draw(img)
            image_font = ImageFont.truetype('msyh.ttf', 50)
            dr.text((0, -10), text, font=image_font, fill="#000000")  # 用设置的字体在0,0的位置插入黑色文字
            imageArray = np.asarray(img).flatten()
            templateDic[value] = imageArray + 0
        return templateDic

    def distinguish(self,fontPath):
        dic = {}
        font = TTFont(fontPath)
        uniList = font['cmap'].tables[0].ttFont.getGlyphOrder()
        arr = [eval("u'\\\\u" + uni[3:] + "'") for uni in uniList[1:]]
        arr = list(set(arr))  # 去重
        num = 1
        for value in arr:
            text = bytes(value, 'ascii').decode('unicode_escape')  # 将\ue800这个6位字符串转成一位unicode编码
            im = Image.new("1", (50, 50), 1)  # 生成一张25*50白底的图片
            dr = ImageDraw.Draw(im)  # 开始画图
            image_font = ImageFont.truetype(fontPath, 50)  # 设置字体文件和大小
            dr.text((0, -10), text, font=image_font, fill="#000000")  # 用设置的字体在0,0的位置插入黑色文字
            dic[value] = np.asarray(im).flatten() + 0
            num += 1
        return dic

    def compare(self,imageDicValue, templateDic):
        max = 0
        retCh = ''
        for key, value in templateDic.items():
            temp = self.cos_sim(imageDicValue, value)
            if temp > max:
                max = temp
                retCh = key
        return bytes(retCh, 'ascii').decode('unicode_escape')

    def cos_sim(self,vector_a, vector_b):
        """
        计算两个向量之间的余弦相似度
        :param vector_a: 向量 a
        :param vector_b: 向量 b
        :return: sim
        """
        vector_a = np.mat(vector_a)
        vector_b = np.mat(vector_b)
        try:
            num = float(vector_a * vector_b.T)
            denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
        except Exception as e:
            print(e)
        cos = num / denom
        sim = 0.5 + 0.5 * cos
        return sim

    def getCommentsFromPage(self,htmlFile):
        soup = BeautifulSoup(open(htmlFile, encoding='utf-8', errors='igonre'), 'html.parser')
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]
        contents = soup.findAll('div', class_='text-con')
        content = contents[-1]
        content = content.text.replace('\n', '')
        content = re.sub('\s+', '', content)
        return content

    def combine(self,templateDic, fontPath, htmlFile):
        dic = self.distinguish(fontPath)
        content = self.getCommentsFromPage(htmlFile)
        specificChDic = {}
        print('一共{n}个需要替换'.format(n=len(dic)))
        num = 1
        for key, value in dic.items():
            v = self.compare(value, templateDic)
            specificChDic[key] = v
            num += 1
        for key, value in specificChDic.items():
            text = bytes(key, 'ascii').decode('unicode_escape')
            content = content.replace(text, value)
        return content

    def listdir(self,path, list_name):  # 传入存储的list
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                self.listdir(file_path, list_name)
            else:
                list_name.append(file_path)

    def outterCall(self,sourcePath):
        templateDic = self.getTemplateFont()
        for entryId, modelIds in self.modelIdDic.items():
            for modelId in modelIds:
                basePath = os.path.join(sourcePath, str(entryId), str(modelId))
                for pageNum in range(1, len([i for i in os.listdir(basePath) if i.endswith('html')]) + 1):
                    entirePath = os.path.join(basePath, str(pageNum))
                    print('正在处理{entirePath}'.format(entirePath=entirePath))
                    content = self.combine(templateDic, '{entirePath}.ttf'.format(entirePath=entirePath),
                                                     '{entirePath}.html'.format(entirePath=entirePath))
                    print('{entirePath}处理完毕,正在保存到文件'.format(entirePath=entirePath))
                    print(content)
                    with open('{entirePath}.txt'.format(entirePath=entirePath, pageNum=pageNum), 'wb') as writer:
                        writer.write(content.encode('utf-8'))
                    print('{entirePath}保存到文件完成'.format(entirePath=entirePath))

# if __name__ == '__main__':
#     modelIdDic = {89: [32342, 32537, 32538]}
#     imageRecognize = ImageRecognize(modelIdDic=modelIdDic)
#     imageRecognize.outterCall()
    # templateDic = imageRecognize.getTemplateFont()
    # for entryId, modelIds in modelIdDic.items():
    #     for modelId in modelIds:
    #         basePath = os.path.join('prizePages', str(entryId), str(modelId))
    #         for pageNum in range(1, len([i for i in os.listdir(basePath) if i.endswith('html')]) + 1):
    #             entirePath = os.path.join(basePath, str(pageNum))
    #             print('正在处理{entirePath}'.format(entirePath=entirePath))
    #             content = imageRecognize.combine(templateDic, '{entirePath}.ttf'.format(entirePath=entirePath),
    #                               '{entirePath}.html'.format(entirePath=entirePath))
    #             print('{entirePath}处理完毕,正在保存到文件'.format(entirePath=entirePath))
    #             print(content)
    #             with open('{entirePath}.txt'.format(entirePath=entirePath, pageNum=pageNum), 'wb') as writer:
    #                 writer.write(content.encode('utf-8'))
    #             print('{entirePath}保存到文件完成'.format(entirePath=entirePath))
