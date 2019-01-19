# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from Spider.xinlang.xinlang import settings


class XinlangPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='19950412', db='xinlang',charset='utf8')  # 打开数据库连接
        self.cursor = self.conn.cursor()  # 使用cursor()方法获取操作游标

    def process_item(self, item, spider):
        # SQL 插入语句
        #sql = """INSERT INTO news(url,column,title,newstime,source,contents,editor) VALUES ('%s','%s','%s','%s','%s','%s','%s')""" \
        #      % (item["x_url"], item["x_column"], item["x_title"], item["x_newstime"],item["x_source"],item["x_contents"],item["x_editor"])
        sql = """INSERT INTO news(linkk,platee,titlee,newstime,sourcee,articlee,editorr) VALUES ('{0:s}','{1:s}','{2:s}','{3:s}','{4:s}','{5:s}','{6:s}')""".format(
            item["x_url"], item["x_column"], item["x_title"], item["x_newstime"],item["x_source"],item["x_contents"],item["x_editor"])
        #self.cursor.execute(sql)
        #self.conn.commit()
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            return item
        except:
            # Rollback in case there is any error
            print("""
            
            
            mysql-------error
            
            
            
            """)
            self.conn.rollback()


    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()