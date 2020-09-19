from random import randint
from time import sleep

import scrapy
from scrapy.selector import Selector
from valkyrie_worker.items import ValkyriePhoneItem, ValkyriePhoneCommentItem


class ValkyrieSpiderSpider(scrapy.Spider):
    name = 'valkyrie_spider'
    allowed_domains = ['smzdm.com']
    # 智能手机链接
    start_urls = ['https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/']

    def parse(self, response):
        phones = Selector(response=response).\
            xpath('//li[@class="feed-row-wide"]')

        for phone in phones:
            phone_title = phone.xpath('.//h5[@class="feed-block-title"]')
            phone_name = phone_title.xpath('.//a/text()').get()
            phone_url = phone_title.xpath('.//a//@href').get()
            yield ValkyriePhoneItem({
                'name': phone_name,
                'url': phone_url
            })

            sleep(randint(1, 5))  # Add a random sleep
            yield response.follow(url=phone_url,
                                  callback=self.parse_comments)

    def parse_comments(self, response):
        # phone title
        title = Selector(response=response).\
            xpath('//h1[@class="title J_title"]/text()').get().strip()
        # content list
        comments = Selector(response=response).\
            xpath('//li[@class="comment_list"]')

        for comment in comments:
            comment_wrap = comment.\
                xpath('.//div[@class="comment_conWrap"]')
            comment_content = comment_wrap.\
                xpath('.//span[@itemprop="description"]/text()').get()
            yield ValkyriePhoneCommentItem({
                'phone': title,
                'content': comment_content
            })
