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
    x_newstime = scrapy.Field()  # 新闻发布时间
    x_source = scrapy.Field()  # 发布源
    x_contents = scrapy.Field()
    x_editor = scrapy.Field()
