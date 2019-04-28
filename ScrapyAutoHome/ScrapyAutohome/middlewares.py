# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Selector
import time, logging
from scrapy.conf import settings
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from fake_useragent import UserAgent


class RandomUserAgentMiddleware(object):

    def __init__(self):
        self.agent = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.agent.random)


class ABProxyMiddleware(HttpProxyMiddleware):
    # """ 阿布云ip代理配置 """

    def process_request(self, request, spider):
        request.meta['splash']['args']['proxy'] = 'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_SERVER}'.format(
            PROXY_USER=settings['PROXY_USER'], PROXY_PASS=settings['PROXY_PASS'], PROXY_SERVER=settings['PROXY_SERVER'])


class ScrapyautohomeSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if (response.status in self.retry_http_codes) or response.status == 302:
            # time.sleep(random.randint(50, 100))
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        if response.status == 200:
            selector = Selector(response)
            authen = selector.xpath('//title/text()').extract_first()
            if '429 Too Many Requests' in authen:
                logging.warning('429 Too Many Requests')
                reason = response_status_message(response.status) + "'429 Too Many Requests'"
                time.sleep(1)
                return self._retry(request, reason, spider) or response
            elif "503 Service Unavailable" in response.text:
                logging.warning('503 Service Unavailable')
                reason = response_status_message(response.status) + "503 Service Unavailable"
                time.sleep(1)
                return self._retry(request, reason, spider) or response
            elif "404 - File or directory not found." in response.text:
                logging.warning('404 - File or directory not found.')
                reason = response_status_message(response.status) + "404 - File or directory not found."
                time.sleep(0.5)
                return self._retry(request, reason, spider) or response
            if (authen is not None and '安全认证' in authen) or '加载验证码' in response.text:
                # time.sleep(random.randint(30, 90))
                reason = response_status_message(response.status) + '遇到了验证码'
                return self._retry(request, reason, spider) or response
            elif 'detail' in response.url:
                # 没遇到验证码也可能页面有问题
                contents = selector.xpath("//div[contains(@class,'koubei-final')]")
                allCommentsNum = selector.xpath('//span[@id="Comment_{commentsId}"]//text()'.format(
                    commentsId=response.meta['commentsId']))
                if len(contents) == 0 or len(allCommentsNum) == 0:
                    reason = response_status_message(response.status) + '没遇到验证码，但是页面有问题，需要重新获取'
                    return self._retry(request, reason, spider) or response
            return response


class ScrapyautohomeDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        pass

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
