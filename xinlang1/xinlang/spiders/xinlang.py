# -*- coding: utf-8 -*-

import re
from scrapy import Request
from Spider.xinlang.xinlang.items import XinlangItem
from lxml import etree
from scrapy_splash import SplashRequest
from scrapy_redis.spiders import RedisSpider


class XinlangSpider(RedisSpider):
    name = 'xinlang'
    #redis_key = 'myspider:start_urls'  # 可以用redis实现分布式，介绍网页https://github.com/rmax/scrapy-redis
    start_urls = ['http://finance.sina.com.cn/roll/#pageid=384&lid=2519&k=&num=50&page=1']
    # 这个网址是新浪财经feed流的网址，可以通过浏览器‘检查--NetWork’或者用Fiddler抓包得到，这个网址直接返回很多内容，包括全部新闻的网址
    # allowed_domains = ['http://finance.sina.com.cn/']


    # 从start_requests发送请求
    def start_requests(self):
        link = self.start_urls[0]
        yield Request(url=link , callback=self.parse)

    def parse(self,response):
        # url = response.url
        url1 = 'http://finance.sina.com.cn/roll/#pageid=384&lid=2519&k=&num=50&page=1'
        # url = url1[:-1]+str(2)
        # yield SplashRequest(url=url1, callback=self.parse1, endpoint='render.html', args={'wait': 1.0},
                            #meta={'lab':1,'wangzhi':url1})
        script = """
        function main(splash, args)
          assert(splash:go(args.url))
          assert(splash:wait(1.0))
          local res = splash:html()
          local a = splash:select_all('.pagebox_pre > a')[1]
          assert(a:mouse_click())
          assert(splash:wait(1.0))
          local res1 = splash:html()
          local b = splash:select_all('.pagebox_pre > a')[2]
          assert(b:mouse_click())
          assert(splash:wait(1.0))
          local res2 = splash:html()
          return { res=res,res1=res1,res2=res2 }
        end
        """
        script1 = """
        function main(splash, args)
          assert(splash:go(args.url))
          assert(splash:wait(4.0))
          local res = splash:html()
          return { res = splash:html() }
        end
        """
        yield SplashRequest(url=url1, callback=self.parse1, endpoint='execute', args={'lua_source': script1, 'wait': 2.0,},
                            meta={'lab':1,'wangzhi':url1})
        for i in range(2,20):
            url = url1[:-1] + str(i)
            script1 = """
            function main(splash, args)
              assert(splash:go(args.url))
              assert(splash:wait(4.0))
              local res = splash:html()
              return { res = splash:html() }
            end
            """
            yield SplashRequest(url=url, callback=self.parse1, endpoint='execute', args={'lua_source': script1, 'wait': 2.0,},
                            meta={'lab':1,'wangzhi':url})

    def parse1(self, response):
        lab = response.meta['lab']
        # print(response.body.decode('utf-8'))
        """url = response.url
        out = open('d:\\pic\\findme.txt','a')
        out.write(url)
        out.write('\n')
        out.close()"""

        for i in (response.data['res'],):
            print(i)
            body = etree.HTML(i)
            a = body.xpath("//div[@class='d_list_txt']/ul/li/span[2]/a/@href")
            for url in a:
                yield SplashRequest(url = url, callback = self.parse2, endpoint='render.html',args={'wait': 1.0})
            # 下面暂时没有用
            if lab == 2:
                script = """
                function main(splash, args)
                  assert(splash:go(args.url))
                  assert(splash:wait(0.5))
                  local a = splash:select_all('.pagebox_pre > a')[2]
                  assert(a:mouse_click())
                  assert(splash:wait(1))
                  return html = splash:html()
                end
                """
                yield SplashRequest(url=response.meta['wangzhi'], callback=self.parse1, endpoint='execute', args={'lua_source': script, 'wait': 1.0},
                                    meta={'lab': 2})


    def parse2(self,response):
        body = etree.HTML(response.body.decode('utf-8'))
        item = XinlangItem()
        item['x_url'] = str(response.url)
        item['x_column'] = str(u'财经')
        # item['x_title'] = body.xpath("//h1[@class='main-title']/text()")[0]
        # item['x_newstime'] = body.xpath("//div[@class='date-source']/span[1]/text()")[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', '')
        # item['x_source'] = body.xpath("//div[@class='date-source']/span[2]/text()")[0]
        item['x_title'] = str(body.xpath("//meta[@property='og:title']/@content")[0])
        item['x_newstime'] = str(body.xpath("//meta[@name='weibo: article:create_at']/@content")[0])
        item['x_source'] = str(body.xpath("//meta[@name='mediaid']/@content")[0])
        d = body.xpath("//div[@class='article' and @id='artibody']/p")
        e = d[0].xpath("string(.)")
        art = str(e).replace('\t', '').replace('\n', '').replace('\u3000', '\n')  #
        item['x_contents'] = art
        item['x_editor'] = re.findall(u'责任编辑：(.+)',art)[0]
        yield item
