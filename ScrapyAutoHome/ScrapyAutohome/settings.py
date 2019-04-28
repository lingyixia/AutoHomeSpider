# -*- coding: utf-8 -*-

# Scrapy settings for ScrapyAutohome project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ScrapyAutohome'

SPIDER_MODULES = ['ScrapyAutohome.spiders']
NEWSPIDER_MODULE = 'ScrapyAutohome.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
#     'Cookie': '__ah_uuid=6E2EE750-AD48-4118-870B-20D278B6EAF6; fvlid=15306094210781UPB8GXxry; sessionid=7527298E-2311-4801-A9B5-ADB118CCEAF2%7C%7C2018-07-03+17%3A17%3A01.710%7C%7Cwww.baidu.com; sessionuid=7527298E-2311-4801-A9B5-ADB118CCEAF2%7C%7C2018-07-03+17%3A17%3A01.710%7C%7Cwww.baidu.com; ASP.NET_SessionId=hdrjt4rgfnmqmwijhxkt0wap; __utmc=1; autosessionid=e4f9950b-6ac0-4604-aa04-54ec8654ac6f; guidance=true; isFromQQSearch=; UM_distinctid=1655ba83c69c8b-07cc2bcf10678a-68151275-100200-1655ba83c6a42d; sessionip=121.69.1.10; area=110101; mallsfvi=1537859367149i1BLziwr%7Cev.autohome.com.cn%7C3278545; isFromBaiDuSearch=; Hm_lvt_9924a05a5a75caf05dbbfb51af638b07=1542097144; CNZZDATA1262640694=1118666130-1534840848-%7C1543456562; Hm_lpvt_9924a05a5a75caf05dbbfb51af638b07=1543558219; cnversion=iwvC/IBlHGxcNts1p12x9YOxonlANuvs2nZ6RpLRSYCKzLESpCACwXut8kBw6sZ9/EHBYSmFT5jQ6qjcmEOgA0GzEIzY95Kt6kAAll1v8naTxlHGqt4tsA==; live-voteid=pc315857840754018125; __utma=1.1974983514.1532075524.1545097108.1545270579.10; __utmz=1.1545270579.10.9.utmcsr=club.autohome.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/bbs/thread/915b25f5a807d95e/77670825-1.html; cuserid-winter=1638849335; clubUserShow=498008|692|2|游客|0|0|0||2018-12-21+09:55:01|0; pbcpopclub=7d570576-c24e-48c7-b941-67607262221c; ahpau=1; historybbsName4=c-4073%7C%E6%AF%94%E4%BA%9A%E8%BF%AAe5%2Cc-4744%7C%E6%8E%A2%E5%B2%B3%2Cc-159%7C%E5%AE%9D%E9%A9%ACX5%2Cc-2098%7CAC%20Schnitzer%2Cc-2366%7CABT%2Cc-4362%7CAC%20Schnitzer%20i8%2Ca-100024%7C%E4%B8%8A%E6%B5%B7%2Cc-3230%7C%E5%AE%9D%E9%A9%AC2%E7%B3%BB%2Cc-4838%7C%E5%AE%9D%E9%A9%ACiX3%2Cc-18%7C%E5%A5%A5%E8%BF%AAA6L; sessionvid=5EA32E28-4535-4FD3-929D-F990F72AB847; autoac=6BE535360EFAF51493C366AAA793EDC9; autotc=F39676A3285BB80C96A1D0843E207500; ahpvno=32; _fmdata=0E3PzTNbO8RrxnnPXBxr8rgid%2FpnMtW7b4k3SFiEhK%2BosV%2BBPGD57AJbVz3LySWueldHnWSEM8HIssjc3G5faa1%2FCRKT8I2O2rE8ljez7WQ%3D; pvidchain=3311255,2099126,2112108,2112108; ref=www.baidu.com%7C0%7C0%7C0%7C2019-01-16+11%3A13%3A11.895%7C2019-01-09+13%3A59%3A24.332; ahrlid=15476083888176jDv8u25NW-1547608400597',
# }
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
RETRY_TIMES = 5
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_DELAY = 7  # 每次请求间隔时间
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'ScrapyAutohome.middlewares.ScrapyautohomeSpiderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'ScrapyAutohome.pipelines.ScrapyautohomePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# splash
# 渲染服务的url
SPLASH_URL = 'http://172.20.206.28:8050'

# 下载器中间件
# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'ScrapyAutohome.middlewares.MyRetryMiddleware': 543,
    'ScrapyAutohome.middlewares.RandomUserAgentMiddleware': 1,
    'ScrapyAutohome.middlewares.ABProxyMiddleware': 2,
}
# 去重过滤器
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# 使用Splash的Http缓存
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# mysql相关
MYSQL_HOST = '172.20.206.28'
MYSQL_DBNAME = 'autohomespider'
MYSQL_USER = 'nanwei'
MYSQL_PASSWD = 'nanwei'
MYSQL_PORT = 3306

# MongoDB configuration
MONGODB_HOST = '172.20.206.28'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'koubei'
MONGODB_DOCNAME = 'autohome'

# Log configuration
from datetime import datetime

today = datetime.now()
log_file_path = "./log/koubeiSpider_{}_{}_{}.log".format(today.year, today.month, today.day)
LOG_LEVEL = 'DEBUG'
LOG_FILE = log_file_path

# email
EXTENSIONS = {
    'scrapy.extensions.statsmailer.StatsMailer': 500,
}

# STATSMAILER_RCPTS = ['chinachenfeiyu@outlook.com',]

MAIL_FROM = 'chinachenfeiyu@qq.com'
MAIL_HOST = 'smtp.qq.com'
MAIL_PORT = 25
MAIL_USER = 'chinachenfeiyu@qq.com'
MAIL_PASS = 'qdehztgvyomfbdcb'

""" 阿布云ip代理配置，包括账号密码 """
PROXY_SERVER = "http-dyn.abuyun.com:9020"
PROXY_USER = "HUS9R96F63A2JDHD"
PROXY_PASS = "B56304BDF7DB5FAF"
PROXY_HOST = "http-dyn.abuyun.com"
PROXY_PORT = "9020"
