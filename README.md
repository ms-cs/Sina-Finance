# Sina-Finance
Crawling Sina Finance News with scrapy

xinlang1文件夹使用了Scrapy-Splash，https://github.com/scrapy-plugins/scrapy-splash#configuration

xinlang文件夹不使用Scrapy-Splash，因为后来发现这个feed流网址不需要使用动态网页加载，直接request就行，使用Scrapy-Splash实在是效率太慢！！
