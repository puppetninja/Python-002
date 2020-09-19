# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ValkyriePhoneItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()


class ValkyriePhoneCommentItem(scrapy.Item):
    phone = scrapy.Field()
    content = scrapy.Field()
