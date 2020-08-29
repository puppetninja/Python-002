import scrapy
from douban_scrapy.items import DoubanScrapyItem
from scrapy.selector import Selector


class MovieSpiderSpider(scrapy.Spider):
    name = 'movie_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']
    rating_level = ['很差', '较差', '还行', '推荐', '力荐']

    def start_requests(self):
        for i in range(0, 10):
            # 电影八百影评
            url = f'https://movie.douban.com/subject/26754233/comments?start={i*20}&limit=20&sort=new_score&status=P'
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        reviews = Selector(response=response).xpath('//div[@class="comment-item"]')  # noqa: E501

        for review in reviews:
            comment_info = \
                review.xpath('.//span[@class="comment-info"]')
            comment_rate = comment_info.xpath('./span[2]/@title').get()

            if comment_rate in self.rating_level:
                yield DoubanScrapyItem({
                    'rating': comment_rate,
                    'comment': review.xpath('.//span[@class="short"]/text()').extract()[0]
                })
