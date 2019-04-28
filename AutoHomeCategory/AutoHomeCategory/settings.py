# -*- coding: utf-8 -*-

# Scrapy settings for AutoHomeCategory project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'AutoHomeCategory'

SPIDER_MODULES = ['AutoHomeCategory.spiders']
NEWSPIDER_MODULE = 'AutoHomeCategory.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# Obey robots.txt rules
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_DELAY = 10  # 每次请求间隔时间
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 302]
# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Cookie': '__ah_uuid=1C080609-3A66-49F5-AA51-4C0D649020FD; fvlid=1537456664613lN7cXLVYzb; sessionid=B54596DD-E0C9-4199-B3DC-B2FCA81AF63B%7C%7C2018-09-20+22%3A17%3A48.155%7C%7Cwww.baidu.com; sessionuid=B54596DD-E0C9-4199-B3DC-B2FCA81AF63B%7C%7C2018-09-20+22%3A17%3A48.155%7C%7Cwww.baidu.com; ASP.NET_SessionId=xwpozmdi0hjb0oun55h43nrw; cookieCityId=110100; guidance=true; UM_distinctid=166e8e47ada288-0cabe83163694d-b79183d-100200-166e8e47adbf42; CNZZDATA1262640694=1023170808-1541500259-%7C1541505680; historybbsName4=c-2951%7C%E5%A5%A5%E8%BF%AAQ3%2Cc-692%7C%E5%A5%A5%E8%BF%AAA4L%2Cc-3170%7C%E5%A5%A5%E8%BF%AAA3%2Cc-2561%7C%E5%AE%9D%E9%A9%ACX1%2Cc-4274%7C%E9%80%94%E8%A7%82%2F%E9%80%94%E8%A7%82L%2Cc-3248%7C%E5%A5%94%E9%A9%B0GLA%2Cc-4080%7C%E8%8D%A3%E5%A8%81RX5%2FRX5%E6%96%B0%E8%83%BD%E6%BA%90%2Cc-4073%7C%E6%AF%94%E4%BA%9A%E8%BF%AAe5; area=130930; ahpau=1; pbcpopclub=112251b0-7a86-48b8-932e-be84c553caf8; sessionip=223.104.101.2; sessionvid=E94042F7-36C0-4D0B-8594-2F4E78857CB5; autoac=0F761F3A5C8F16CFD779857B480AAE01; autotc=285B22B68870F11FC0E105B1FEC41776; pvidchain=3311255,2099126; ahpvno=48; _fmdata=fi46RLYz9UERsANGMWVwdKrLTx%2FZc5lSz9qcWXY3cl2xvY8FT%2B6FxSMGIgSnzOrr2AXBKyEKOIcilOkNr9r%2BR9BxAuC1KT8yU28eoggwRxs%3D; ref=www.baidu.com%7C0%7C0%7C0%7C2019-02-09+21%3A21%3A17.358%7C2019-02-04+14%3A55%3A50.294; ahrlid=1549718475021J2CysJTa5G-1549718477766'
}
# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'AutoHomeCategory.middlewares.AutohomecategorySpiderMiddleware': 543,
# }
# REDIRECT_ENABLED = False
# HTTPCACHE_ENABLED = True
# HTTPERROR_ALLOWED_CODES = [302]
# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'AutoHomeCategory.middlewares.MyRetryMiddleware': 543,
    'AutoHomeCategory.middlewares.ProxyMiddleware': 1,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'AutoHomeCategory.pipelines.AutohomecategoryPipeline': 300,
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
MONGODB_DOCNAME = 'autohometagedentire'

from datetime import datetime

today = datetime.now()
log_file_path = "./log/categorySpider_{}_{}_{}.log".format(today.year, today.month, today.day)
LOG_LEVEL = 'DEBUG'
LOG_FILE = log_file_path
# """ 阿布云ip代理配置 """
# Agent
""" 阿布云ip代理配置，包括账号密码 """
PROXY_SERVER = "http://http-dyn.abuyun.com:9020"
PROXY_USER = "HUS9R96F63A2JDHD"
PROXY_PASS = "B56304BDF7DB5FAF"
PROXY_HOST = "http-dyn.abuyun.com"
PROXY_PORT = "9020"
