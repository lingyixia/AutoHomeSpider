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
        arr = ['五', '长', '级', '外', '养', '灯', '来', '中', '真', '大', '自', '音', '四', '近', '只', '是', '里', '冷', '味', '路',
               '皮', '七', '和', '档', '排', '控', '上', '性', '孩', '当', '更', '加', '不', '电', '十', '低', '了', '好', '一', '六', '右',
               '开', '二', '油', '着', '少', '问', '小', '响', '硬', '软', '的', '下', '很', '远', '手', '门', '机', '副', '多', '光', '比',
               '保', '地', '三', '身', '坐', '实', '盘', '短', '雨', '得', '坏', '启', '九', '过', '无', '内', '泥', '呢', '空', '八', '公',
               '耗', '量', '左', '有', '矮', '高', '动']
        for value in arr:
            img = Image.new('1', (50, 50), 1)
            dr = ImageDraw.Draw(img)
            image_font = ImageFont.truetype('./msyh.ttf', 50)
            dr.text((0, -10), value, font=image_font, fill="#000000")  # 用设置的字体在0,0的位置插入黑色文字
            data = img.getdata()
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
        cos = num / denom
        sim = 0.5 + 0.5 * cos
        return sim

    def combine(self, templateDic):
        dic = self.distinguish(self.orignFont)
        specificChDic = {}
        logging.info('一共{n}个需要替换'.format(n=len(dic)))
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
