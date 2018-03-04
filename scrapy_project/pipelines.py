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
from scrapy.http import Request

class SpiderMeizituPipeline(ImagesPipeline):
    @classmethod
    def get_media_requests(self, item, info):
        return Request(item['image_urls'][0],meta={'imagegroup':item['images'],'imageindex':item['index']})

    def file_path(self, request, response=None, info=None):
        
        print('SpiderMeizituPipeline -->> request:::',request)
        imagegroup = request.meta['imagegroup']
        imageindex = request.meta['imageindex']
        filepath = 'full/%s/%s.jpg' % (imagegroup,imageindex)
       
        return filepath
