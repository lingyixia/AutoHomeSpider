from fontTools.ttLib import TTFont
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import logging, json


# 获取模板字符集中的对应关系，只需运行一次即可
class ImageRecognizer:
    def __init__(self, orignText, orignFont):
        self.orignText = orignText
        self.orignFont = orignFont

    def getTemplateFont(self):
        templateDic = {}
        arr = ['短', '下', '七', '得', '八', '四', '上', '一', '左', '小', '很', '大', '长', '是', '右', '三', '九', '呢', '着', '坏',
               '地', '了', '的', '远', '和', '高', '五', '六', '十', '不', '少', '多', '更', '矮', '近', '二', '好', '低']
        for value in arr:
            img = Image.new('1', (50, 50), 1)
            dr = ImageDraw.Draw(img)
            image_font = ImageFont.truetype('./msyh.ttf', 50)
            dr.text((0, -10), value, font=image_font, fill="#000000")  # 用设置的字体在0,0的位置插入黑色文字
            # img.save('./template/'+value+'.png')
            data = img.getdata()
            # data = np.matrix(data, dtype=np.int32) / 255
            templateDic[value] = np.array(data) / 255
        return templateDic

    def distinguish(self, fontPath):
        dic = {}
        font = TTFont(fontPath)
        uniList = font['cmap'].tables[0].ttFont.getGlyphOrder()
        arr = [eval("u'\\\\u" + uni[3:] + "'") for uni in uniList[1:]]
        arr = list(set(arr))  # 去重
        num = 1
        for value in arr:
            text = bytes(value, 'ascii').decode('unicode_escape')  # 将\ue800这个6位字符串转成一位unicode编码
            img = Image.new("1", (50, 50), 1)  # 生成一张25*50白底的图片
            dr = ImageDraw.Draw(img)  # 开始画图
            image_font = ImageFont.truetype(fontPath, 50)  # 设置字体文件和大小
            dr.text((0, -10), text, font=image_font, fill="#000000")  # 用设置的字体在0,0的位置插入黑色文字
            data = img.getdata()
            # data = np.matrix(data, dtype=np.int32) / 255
            dic[value] = np.array(data) / 255
            num += 1
        return dic

    def compare(self, imageDicValue, templateDic):
        max = 0
        retCh = ''
        for key, value in templateDic.items():
            temp = self.cos_sim(imageDicValue, value)
            if temp > max:
                max = temp
                retCh = key
        # return bytes(retCh, 'ascii').decode('unicode_escape')
        return retCh

    def cos_sim(self, vector_a, vector_b):
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
            logging.warning(e)
            # print(e)
        cos = num / denom
        sim = 0.5 + 0.5 * cos
        return sim

    def combine(self, templateDic):
        dic = self.distinguish(self.orignFont)
        specificChDic = {}
        logging.info('一共{n}个需要替换'.format(n=len(dic)))
        # print('一共{n}个需要替换'.format(n=len(dic)))
        for key, value in dic.items():
            v = self.compare(value, templateDic)
            text = bytes(key, 'ascii').decode('unicode_escape')
            specificChDic[text] = v
        content = self.orignText
        for key, value in specificChDic.items():
            content = content.replace(key, value)
        logging.info('替换完成')
        # print('替换完成')
        return content

    def outterCall(self):
        templateDic = self.getTemplateFont()
        content = self.combine(templateDic)
        return content
