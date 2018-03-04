from scrapy import Request
from scrapy.spiders import Spider
from scrapy_project.items import SpiderMeizituItem
import re

from scrapy_project.settings import IMAGES_STORE


class MeizituSpider(Spider):
    name = 'meizitu'
    
    start_urls = {
        'http://www.meizitu.com/a/more_1.html',
    }

    def parse(self, response):
        meizi_pic_lists = response.xpath('//ul[@class="wp-list clearfix"]/li')
        for i, meizi_item in enumerate(meizi_pic_lists):
            meizi_item_url = meizi_item.xpath('.//h3[@class="tit"]/a/@href').extract()[0]
            yield Request(meizi_item_url,callback=self.parse_meizi_pic)

        next_url = re.findall('<a href="(.*)">下一页</a>',response.xpath('//*[@id="wp_page_numbers"]').extract()[0])
        print('next_url:::::',next_url)

        if next_url:
            next_url = 'http://www.meizitu.com/a/' + next_url[0]
            yield Request(next_url,callback=self.parse)
 
    def parse_meizi_pic(self,response):
        item = SpiderMeizituItem()
        meizitu_pics = response.xpath('//div[@id="picture"]/p/img')
        
        for i, meizitu_pic in enumerate(meizitu_pics):
            item['index'] = str(i+1)
            item['images'] = meizitu_pic.xpath('.//@alt').extract()[0].split('，')[0]
            item['image_urls'] = meizitu_pic.xpath('.//@src').extract()
            yield item
        
