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
        #print('response:::',response)
        meizi_pic_lists = response.xpath('//ul[@class="wp-list clearfix"]/li')
        #print('meizi_pic_lists:::',meizi_pic_lists)
        for i, meizi_item in enumerate(meizi_pic_lists):
            meizi_item_url = meizi_item.xpath('.//h3[@class="tit"]/a/@href').extract()[0]
            print('===== 当前爬取页面共有图片%s组，正在抓取第%s组图片，页面链接:: %s ====='% (len(meizi_pic_lists),i+1,meizi_item_url))
            yield Request(meizi_item_url,callback=self.parse_meizi_pic)

        next_url = re.findall('<a href="(.*)">下一页</a>',response.xpath('//*[@id="wp_page_numbers"]').extract()[0])
        print('next_url:::::',next_url)
        #print('response:::::',response.xpath('//*[@id="wp_page_numbers"]').extract()[0])

        if next_url:
            next_url = 'http://www.meizitu.com/a/' + next_url[0]
            print('========== Request Next Url :: %s ==========' % next_url )
            yield Request(next_url,callback=self.parse)
        

    def parse_meizi_pic(self,response):
        print('========== parse_meizi_pic response::: %s =========='% response)
        item = SpiderMeizituItem()
        meizitu_pics = response.xpath('//div[@id="picture"]/p/img')
        
        for i, meizitu_pic in enumerate(meizitu_pics):
            image_group = meizitu_pic.xpath('.//@alt').extract()[0].split('，')[0]
            item['images'] = image_group
            #item['image_paths'] = IMAGES_STORE + '/' + image_group + '/' + image_group + str(i) + '.jpg'
            item['image_urls'] = meizitu_pic.xpath('.//@src').extract()
            
            print('===== 当前页面共有图片%s张，正在抓取第%s张图片 ====='% (len(meizitu_pics),i+1))
            print('===== 图片链接:: %s ====='% (item['image_urls']))
            print('===== 存储路径:: %s ====='% (item['image_paths']))
            yield item
        
