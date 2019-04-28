# -*- coding: utf-8 -*-

# Scrapy settings for autohomeForum project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'autohomeForum'

SPIDER_MODULES = ['autohomeForum.spiders']
NEWSPIDER_MODULE = 'autohomeForum.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
RETRY_TIMES = 5
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_DELAY = 5  # 每次请求间隔时间
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
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'autohomeForum.middlewares.AutohomeforumSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
RANDOM_UA_TYPE = 'random'
# 渲染服务的url
SPLASH_URL = 'http://172.20.206.28:8050'
RETRY_TIMES = 10

# 下载器中间件
# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'autohomeForum.middlewares.MyRetryMiddleware': 543,
    'autohomeForum.middlewares.RandomUserAgentMiddleware': 532,
    'autohomeForum.middlewares.ABProxyMiddleware': 1,
}
# 去重过滤器
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# 使用Splash的Http缓存
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'autohomeForum.pipelines.AutohomeforumPipeline': 300,
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
# Log configuration
from datetime import datetime

today = datetime.now()
log_file_path = "./log/forumSpider_{}_{}_{}.log".format(today.year, today.month, today.day)
LOG_LEVEL = 'DEBUG'
#LOG_FILE = log_file_path
# MongoDB configuration
MONGODB_HOST = '172.20.206.28'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'forum'
MONGODB_DOCNAME = 'autohome'

# """ 阿布云ip代理配置 """
# Agent
""" 阿布云ip代理配置，包括账号密码 """
PROXY_SERVER = "http-dyn.abuyun.com:9020"
PROXY_USER = "HD8NW3E5508AJURD"
PROXY_PASS = "42B6A429E1283A39"
PROXY_HOST = "http-dyn.abuyun.com"
PROXY_PORT = "9020"
