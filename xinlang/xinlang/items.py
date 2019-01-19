# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XinlangItem(scrapy.Item):
    #define the fields for your item here like:
    #name = scrapy.Field()
    x_url = scrapy.Field()
    x_column = scrapy.Field()  # 栏目
    x_title = scrapy.Field()
    x_ctime = scrapy.Field()  # 新闻发布时间
    x_mtime = scrapy.Field()
    x_intime = scrapy.Field()
    x_contents = scrapy.Field()
    x_author = scrapy.Field()
    x_level = scrapy.Field()
    x_keywords = scrapy.Field()
    x_lids = scrapy.Field()
    x_media_name = scrapy.Field()
    x_intro = scrapy.Field()
    x_summary = scrapy.Field()
    x_oid = scrapy.Field()
    x_hqChart = scrapy.Field()

