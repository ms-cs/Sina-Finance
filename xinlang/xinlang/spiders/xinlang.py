# -*- coding: utf-8 -*-

import re
from scrapy import Request
from Spider.xinlang.xinlang.items import XinlangItem
from lxml import etree
from scrapy_redis.spiders import RedisSpider
import json
import time

class XinlangSpider(RedisSpider):
    name = 'xinlang'
    redis_key = 'myspider:start_urls'
    # start_urls = ['http://finance.sina.com.cn/roll/#pageid=384&lid=2519&k=&num=50&page=1']
    # allowed_domains = ['http://finance.sina.com.cn/']


    # 从start_requests发送请求
    def start_requests(self):
        link = start_urls
        h = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Referer': 'None',
        }
        yield Request(url=link , callback=self.parse,headers=h)

    def parse(self,response):
        links = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=384&lid=2519&k=&num=50&page=1'
        for i in range(1,5000):
            page = 'page={0:s}'.format(str(i))
            link = links.replace('page=1',page)
            h = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Referer': 'None',
            }
            yield Request(url=link , callback=self.parse1,headers=h)

    def parse1(self,response):
        item = XinlangItem()
        c = json.loads(response.body)
        print("""
        
        
        
        """)
        print(c)
        print("""
        
        
        
        
        """)
        for i in c['result']['data']:
            url = i['wapurl'].replace('http','https')
            item['x_title'] = i['title']
            item['x_url'] = url
            a = i['ctime']
            b = i['mtime']
            c = i['intime']
            timeArraya = time.localtime(int(a))
            timeArrayb = time.localtime(int(b))
            timeArrayc = time.localtime(int(c))
            item['x_ctime'] = time.strftime("%Y-%m-%d %H:%M:%S", timeArraya)
            item['x_mtime'] = time.strftime("%Y-%m-%d %H:%M:%S", timeArrayb)
            item['x_intime'] = time.strftime("%Y-%m-%d %H:%M:%S", timeArrayc)
            item['x_column'] = str(u'财经')
            item['x_author'] = i['author']
            item['x_level'] = i['level']
            item['x_keywords'] = i['keywords']
            item['x_lids'] = i['lids']
            item['x_media_name'] = i['media_name']
            item['x_intro'] = i['intro']
            item['x_summary'] = i['summary']
            item['x_oid'] = i['oid']
            item['x_hqChart'] = i['hqChart']
            yield Request(url=url, callback=self.parse2, meta={'item':item})

    def parse2(self,response):
        body = etree.HTML(response.body.decode('utf-8'))
        item = response.meta['item']
        # item['x_url'] = str(response.url)
        # item['x_column'] = str(u'财经')
        # item['x_title'] = body.xpath("//h1[@class='main-title']/text()")[0]
        # item['x_newstime'] = body.xpath("//div[@class='date-source']/span[1]/text()")[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', '')
        # item['x_source'] = body.xpath("//div[@class='date-source']/span[2]/text()")[0]
        # item['x_title'] = str(body.xpath("//meta[@property='og:title']/@content")[0])
        # item['x_newstime'] = str(body.xpath("//meta[@name='weibo: article:create_at']/@content")[0])
        # item['x_source'] = str(body.xpath("//meta[@name='mediaid']/@content")[0])
        d = body.xpath("//article[@class='art_box']/p[@class='art_p']")
        art = ''
        for i in d:
            art += '\n'
            art += i.xpath("string(.)").replace('\u3000', '')
        # art = str(e).replace('\t', '').replace('\n', '').replace('\u3000', '\n')
        item['x_contents'] = art
        # item['x_editor'] = re.findall(u'责任编辑：(.+)',art)[0]
        yield item
