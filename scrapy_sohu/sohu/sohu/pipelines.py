# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import pymssql
import logging


logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class CheckPipline(object):
    def open_spider(self, spider):
        logger.info('spider %s opened' % spider.name)

    def close_spider(self, spider):
        logger.info('spider %s closed' % spider.name)

class SohuPipeline(object):
    def __init__(self):
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        self.conn = pymssql.connect(
            host = '192.168.3.152:4000',
            user = '***',
            password = '***',
            database = 'BaseData2017',
            charset = 'utf8',
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        cols, values = zip(*item.items())
        sql = "insert into ArticleCrawler(%s) values(%s)" %(','.join(cols), ','.join(['%s'] * len(cols)))
       # sql = "insert into ArticleCrawler(SourceType,Source_ID,Status,Category_ID,Title,Favorites,Url,Source,Author,ReadCounts,Content,PublishTime) values('%s','%d','%d','%d','%s','%d','%s','%s','%s','%d','%s','%s')"%(item['SourceType'],item['Source_ID'],item['Status'],item['Category_ID'],item['Title'],item['Favorites'],item['Url'],item['Source'],item['Author'],item['ReadCounts'],item['Content'],item['PublishTime'])
        self.cur.execute(sql, values)
        self.conn.commit()
        logger.info(self.cur._last_executed)
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

