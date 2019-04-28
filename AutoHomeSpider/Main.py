from AutoHomeSpider import AutoHomePrizeSpider
from selenium import webdriver

if __name__ == '__main__':
    baseUrl = 'https://k.autohome.com.cn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
    }
    modelIdDic = {65: [31845, 31848, 31844, 31840, 31846, 31847, 31548, 31842, 31843, 31804, 31841],
                  66: [29318, 29315, 29319, 29317, 29316, 29314, 29320],
                  67: [32004, 34169, 32001, 31997, 32003, 34170, 29096, 31996, 31998, 31999, 31860, 31861, 32891],
                  68: [31148, 31153, 31152, 31150, 31151, 31149],
                  70: [28226, 29754, 28224, 28225, 28227, 33307, 28223, 33308, 33310, 29753, 33309],
                  71: [28882, 28891, 34279, 28880, 34276, 28892, 34148, 34149, 28617, 28619, 28618, 28684],
                  72: [31067, 31060, 28408, 28409, 31062, 31061, 31065, 31064, 27187, 31059, 31058, 31063, 28535, 27186,
                       28410, 31066, 28411]}

    autoHomePrizeSpider = AutoHomePrizeSpider(baseUrl=baseUrl, headers=headers, modelIdDic=modelIdDic,
                                              sourcePath='prizePages', savePath='export_koubei_article_multi')
    # autoHomePrizeSpider.getEntirePageUrl()
    # driver = webdriver.Chrome(
    #     executable_path='C:\\Users\\chenfeiyu1\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe')
    # autoHomePrizeSpider.getModelEntirePrize(driver=driver)
    autoHomePrizeSpider.imageRecognize()
    autoHomePrizeSpider.leftBar()
