#弃用，在AutoHomeSpider中
import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import random
import json, random

baseurl = 'https://k.autohome.com.cn'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
}


# 直接获取完整评价页面的url，保存在urls/entryID.json中
def getEntirePages(entryID, modelID):
    entireUrls = {}
    for id in modelID:
        num = 1
        entireUrl = []
        url = '{baseurl}/spec/{modelid}'.format(baseurl=baseurl, modelid=id)
        time.sleep(random.randint(3, 10))
        content = requests.get(url, headers=headers).content
        soup = BeautifulSoup(content, 'html.parser')
        entireDiv = soup.findAll('div', class_='allcont')
        for url in entireDiv:
            entireUrl.append('https:{url}'.format(url=url.find('a').get('href')))
        print('%d第%d页地址收集完成,正在转下一页' % (id, num))
        ifHasNext = soup.find('a', class_='page-item-next')
        while ifHasNext:
            num += 1
            href = ifHasNext.get('href')
            nextPageUrl = '{baseurl}{url}'.format(baseurl=baseurl, url=href)
            time.sleep(random.randint(3, 10))
            content = requests.get(url=nextPageUrl, headers=headers).content
            soup = BeautifulSoup(content, 'html.parser')
            entireDiv = soup.findAll('div', class_='allcont')
            for url in entireDiv:
                entireUrl.append('https:{url}'.format(url=url.find('a').get('href')))
            print('%d第%d页地址收集完成,正在转下一页' % (id, num))
            ifHasNext = soup.find('a', class_='page-item-next')
            tag = soup.find('a', class_='page-disabled page-item-next')
            if tag:
                break
        print('没有下一页了,%d地址收集完成,正在转下一个车型' % (id,))
        entireUrls[id] = entireUrl
    with open(os.path.join('urls',str(entryID)+'.json'), 'w') as writer:
        json.dump(entireUrls, writer, ensure_ascii=False)


if __name__ == '__main__':
    modelIdDic = {60: [32894, 32895, 32897, 32893, 32898, 32892, 32896],
                  58: [32018, 32019, 32016, 32014, 32015, 32017],
                  64: [29093, 29089, 33896, 29092, 33678, 29946, 29096, 25191, 25190, 29094, 29095, 29097, 32828, 25189,
                       29945, 32827, 25188],
                  63: [34851, 34854, 34853, 34856, 34855, 34646],
                  62: [23395, 23394, 31923, 23396, 31925, 31924, 31921, 31922, 22450, 23393],
                  61: [34704, 34703, 30965, 30964, 30962, 30963, 30961],
                  59: [31525, 31524, 31526, 31523, 31529, 31530, 31527],

                  57: [32047, 32046, 32044, 32048, 32050, 32051, 32049, 32040, 32041, 32045, 32043, 32042]}
    for key, value in modelIdDic.items():
        getEntirePages(key, value)
