# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time, random, logging
from scrapy import signals, Selector
from fake_useragent import UserAgent
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import AutoHomeCategory.settings as settings
import base64

proxyAuth = "Basic " + base64.urlsafe_b64encode(
    bytes((settings.PROXY_USER + ":" + settings.PROXY_PASS), "ascii")).decode("utf8")


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        agent = UserAgent()
        request.headers.setdefault('User-Agent', agent.random)
        request.meta["proxy"] = settings.PROXY_SERVER
        request.headers["Proxy-Authorization"] = proxyAuth


class AutohomecategorySpiderMiddleware(object):
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
        if response.status in settings.RETRY_HTTP_CODES:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        if response.status == 200:
            selector = Selector(response)
            authen = selector.xpath('//title/text()').extract_first()
            if '429 Too Many Requests' in authen:
                time.sleep(random.randint(0, 2))
                logging.warning('429 Too Many Requests')
                reason = response_status_message(response.status) + "'429 Too Many Requests'"
                return self._retry(request, reason, spider) or response
            elif "503 Service Unavailable" in response.text:
                time.sleep(random.randint(0, 2))
                logging.warning('503 Service Unavailable')
                reason = response_status_message(response.status) + "503 Service Unavailable"
                return self._retry(request, reason, spider) or response
            elif "404 - File or directory not found." in response.text:
                time.sleep(random.randint(0, 2))
                logging.warning('404 - File or directory not found.')
                reason = response_status_message(response.status) + "404 - File or directory not found."
                return self._retry(request, reason, spider) or response
            elif (authen is not None and '安全认证' in authen) or '加载验证码' in response.text:
                time.sleep(random.randint(0, 2))
                reason = response_status_message(response.status) + ' 遇到了验证码'
                return self._retry(request, reason, spider) or response
            elif 'detail' in response.url:
                # 没遇到验证码也可能页面有问题
                time.sleep(random.randint(0, 2))
                contents = selector.xpath("//div[contains(@class,'koubei-final')]")
                allCommentsNum = selector.xpath('//span[@id="Comment_{commentsId}"]//text()'.format(
                    commentsId=response.meta['commentsId']))
                if len(contents) == 0 or len(allCommentsNum) == 0:
                    reason = response_status_message(response.status) + ' 没遇到验证码，但是页面有问题，需要重新获取'
                    return self._retry(request, reason, spider) or response
            return response


class AutohomecategoryDownloaderMiddleware(object):
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
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

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
