import requests, random, csv, time, os
from bs4 import BeautifulSoup

prizeDic = {'最满意': 10, '最不满意': 11, '空间': 4, '动力': 5, '操控': 6, '油耗': 7, '舒适性': 3, '外观': 1, '内饰': 2, '性价比': 8}
baseUrl = 'https://k.autohome.com.cn/spec'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
}


def parseCatalogue(url, catalogue):
    data = []
    print('正在处理{modelid}{catalogue}'.format(modelid=url.split('/')[-2], catalogue=catalogue))
    testNum = 1  # 测试10次，如果实在获取不到就不要了
    littleTime = 10
    bigTime = 25
    while testNum <= 10:
        try:
            time.sleep(random.randint(littleTime, bigTime))
            content = requests.get(url, headers=headers).content.decode('gbk', errors='ignore')
            break
        except Exception:
            testNum += 1
            if testNum == 11:
                print('去你大爷的老子不要了！！！')
                data.append(url.split('/')[-2])
                data.append('undifined')
                data.append(catalogue)
                data.append('未获取到')
                data.append('未获取到')
                return data
            print('获取出错，正在进行第{testNum}次尝试'.format(testNum=testNum))
            littleTime += 10
            bigTime += 10
    soup = BeautifulSoup(content, 'html.parser')
    soup.find_all()
    negitive = ''
    activite = ''
    try:
        negitive = soup.find('div', class_='revision-impress').findAll('a', class_='dust')[1:]
        negitive = [x.text for x in negitive]
        negitive = ' '.join(negitive)
    except Exception:
        pass
    try:
        activite = soup.find('div', class_='revision-impress').findAll('a', class_='')[1:]
        activite = [x.text for x in activite]
        activite = ' '.join(activite)
    except Exception:
        pass
    data.append(url.split('/')[-2])
    data.append('undifined')
    data.append(catalogue)
    data.append(negitive)
    data.append(activite)
    print('{modelid}{catalogue}处理完毕'.format(modelid=url.split('/')[-2], catalogue=catalogue))
    return data


def saveCSV(datas, num):
    print(datas)
    with open(os.path.join('export_koubei_opinion_summary', str(num) + '.csv'), 'a', newline='') as writer:
        writer = csv.writer(writer)
        writer.writerows(datas)


if __name__ == '__main__':
    modelIdDic = {65: [31845, 31848, 31844, 31840, 31846, 31847, 31548, 31842, 31843, 31804, 31841],
                  66: [29318, 29315, 29319, 29317, 29316, 29314, 29320],
                  67: [32004, 34169, 32001, 31997, 32003, 34170, 29096, 31996, 31998, 31999, 31860, 31861, 32891],
                  68: [31148, 31153, 31152, 31150, 31151, 31149],
                  70: [28226, 29754, 28224, 28225, 28227, 33307, 28223, 33308, 33310, 29753, 33309],
                  71: [28882, 28891, 34279, 28880, 34276, 28892, 34148, 34149, 28617, 28619, 28618, 28684],
                  72: [31067, 31060, 28408, 28409, 31062, 31061, 31065, 31064, 27187, 31059, 31058, 31063, 28535, 27186,
                       28410, 31066, 28411],
                  73: [31247, 31419, 31618, 31422, 31420, 31421, 31423],
                  74: [28883, 28889, 28884, 28886, 30273, 34122, 28885, 28890, 30974, 31814, 31477],
                  75: [32649, 32648, 32647, 34690, 32650, 32645, 32644, 32652, 32653, 34605, 32651],
                  76: [33985, 32851, 33986, 30868, 30876, 31421, 30874, 30875],
                  78: [30495, 33655, 30498, 33660, 33661, 30494, 30489, 30490, 30499, 30496, 30497, 30492, 30493, 30491,
                       33659, 33658, 33657, 33662],
                  79: [27619, 29123, 29124, 27843],
                  80: [34128, 32234, 32235, 32233, 34129, 34127, 32236],
                  81: [29174, 29175, 28814, 33409, 33410, 29173, 29172, 33411, 32582, 33412],
                  82: [29822, 29726, 29823, 29750, 29821, 29825, 29824, 28248, 29826],
                  83: [33335, 33338, 33340, 35276, 33339, 33336, 33337, 35445, 35448, 33341, 35449, 35447]}
    for entryID, modelIDs in modelIdDic.items():
        datas = []
        for modeId in modelIDs:
            for key, value in prizeDic.items():
                url = '{baseurl}/{modeId}/ge{prizedic}'.format(baseurl=baseUrl, modeId=modeId, prizedic=value)
                data = parseCatalogue(url, key)
                datas.append(data)
        saveCSV(datas, str(entryID))
