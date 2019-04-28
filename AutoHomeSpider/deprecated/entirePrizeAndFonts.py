#弃用，在AutoHomeSpider中
from selenium import webdriver
import requests, json, time, random, re, os
from bs4 import BeautifulSoup

baseurl = 'https://k.autohome.com.cn/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
}


# 读取urls中，保存整体页面和字体
def findModelEntirePrize(entryID, driver):
    modelAndUrls = {}
    with open('urls\\{entryID}.json'.format(entryID=entryID), 'r') as reader:
        modelAndUrls = json.load(reader)
    for key in modelAndUrls:
        num = 1
        path = 'prizePages\\{entryID}\\{modelid}'.format(entryID=entryID, modelid=key)
        if not os.path.exists(path):
            os.makedirs(path)
        for url in modelAndUrls[key]:
            driver.get(url)
            time.sleep(random.randint(10, 30))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # 保存字体
            cmp = re.compile("url\('(//.*.ttf)'\) format\('woff'\)")
            rst = cmp.findall(soup.prettify())
            ttf = requests.get("http:" + rst[0], stream=True)
            time.sleep(random.randint(5, 15))
            try:
                with open("{path}/{num}.ttf".format(path=path, num=num), "wb") as pdf:
                    for chunk in ttf.iter_content(chunk_size=1024):
                        if chunk:
                            pdf.write(chunk)
                    print('{modelid}第{num}个字体保存完毕'.format(modelid=key, num=num))
            except Exception as e:
                print(e)
                print('{modelid}第{num}个字体保存失败'.format(modelid=key, num=num))
            try:
                with open("{path}/{num}.html".format(path=path, num=num), "wb") as page:
                    page.write(soup.prettify().encode('utf-8', errors='ignore'))
                    print('{modelid}第{num}个页面保存完毕'.format(modelid=key, num=num))
            except Exception as e:
                print(e)
                print('{modelid}第{num}个页面保存失败'.format(modelid=key, num=num))
            num += 1


if __name__ == '__main__':
    # driver = webdriver.PhantomJS(executable_path='D:\\phantomjs\\bin\\phantomjs.exe')
    driver = webdriver.Chrome(
        executable_path='C:\\Users\\chenfeiyu1\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe')
    modelIds = {64: [29093, 29089, 33896, 29092, 33678, 29946, 29096, 25191, 25190, 29094, 29095, 29097, 32828, 25189,
                     29945, 32827, 25188],
                63: [34851, 34854, 34853, 34856, 34855, 34646],
                62: [23395, 23394, 31923, 23396, 31925, 31924, 31921, 31922, 22450, 23393],
                61: [34704, 34703, 30965, 30964, 30962, 30963, 30961],
                60: [32894, 32895, 32897, 32893, 32898, 32892, 32896],
                59: [31525, 31524, 31526, 31523, 31529, 31530, 31527],
                58: [32018, 32019, 32016, 32014, 32015, 32017],
                57: [32047, 32046, 32044, 32048, 32050, 32051, 32049, 32040, 32041, 32045, 32043, 32042]}
    # modelIds = {48: [29996]}
    for key, value in modelIds.items():
        findModelEntirePrize(key, driver)
