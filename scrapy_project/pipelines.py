# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy_project import settings
import os
import scrapy
import urllib
import time

class SpiderMeizituPipeline(ImagesPipeline):
    print('===== 开启自定义图片下载通道 =====')
    def get_media_requests(self, item, info):
        #print('SpiderMeizituPipeline ----->>>>> item[meizitu_url]:::::',item['meizitu_url'])
        for image_url in item['image_urls']:
           yield scrapy.Request(image_url,meta={'item': item})

    def item_completed(self, results, item, info): 
        image_paths = [x['path'] for ok, x in results if ok] 
        print('image_paths:::',image_paths)
        if not image_paths: 
            raise DropItem("Item contains no images") 
        return item 

    def file_path(self, request, response=None, info=None): 
        item = request.meta['item']

        image_guid = request.url.split('/')[-1]
        filename = u'full/{0[mote_id]}/{1}'.format(item, image_guid)
        print('filename:::',filename)
        return filename


'''
    def process_item(self, item, spider):
        print('========== item item item ==========')
        print('item::::::::::',item)
        image_url = item['meizitu_url']
        dir_path = '%s/%s' % (
            settings.IMAGES_STORE, 
            spider.name 
            )

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        us = image_url.split('/')[5:]
        image_file_name = '_'.join(us)
        file_path = '%s/%s' % (dir_path, image_file_name)

        print('========== urlretrieve start ==========')
        urllib.request.urlretrieve(image_url, file_path)

        return item
'''