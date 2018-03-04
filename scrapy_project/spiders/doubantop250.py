from scrapy import Request
from scrapy.spiders import Spider
from scrapy_project.items import DoubanMovieItem

class DoubanMovieTop250Spider(Spider):
    name = 'doubantop250'
    start_urls = {
        'https://movie.douban.com/top250'
    }
    custom_settings = {
        'ITEM_PIPELINES':{'scrapy_project.pipelines.SpiderDoubanPipeline': 400},
    }



    def parse(self, response):
        item = DoubanMovieItem()
        movies = response.xpath('//ol[@class="grid_view"]/li')
        print(movies)
        print('=============================================')
        for movie in movies:
            item['ranking'] = movie.xpath(
                './/div[@class="pic"]/em/text()').extract()[0]
            item['movie_name'] = movie.xpath(
                './/div[@class="hd"]/a/span[1]/text()').extract()[0]
            item['score'] = movie.xpath(
                './/div[@class="star"]/span[@class="rating_num"]/text()'
            ).extract()[0]
            item['score_num'] = movie.xpath(
                './/div[@class="star"]/span/text()').re(r'(\d+)人评价')[0]
            yield item
        
        next_url = response.xpath('//span[@class="next"]/a/@href').extract()

        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield Request(next_url)