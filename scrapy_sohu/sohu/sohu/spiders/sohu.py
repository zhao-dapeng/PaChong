import scrapy
from scrapy import Request
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from w3lib.html import remove_tags
from sohu.items import SohuItem


def filter(html):
    return remove_tags(html, which_ones=('sup', )).replace('\n', '').replace('\r', '').replace('\t', '')


class SoHuSpider(scrapy.Spider):
    name = "sohu"
    allowed_domains = ["sohu.com"]
    start_urls = ["http://it.sohu.com"]

    def __init__(self, max_num=10, *args, **kwargs):
        super(SoHuSpider, self).__init__(*args, **kwargs)
        self.max_num = int(max_num)

    def parse(self, response):
        links = response.xpath('//*[@id="main-news"]//h4/a/@href').extract()
        for link in links:
            if not link.startswith('//www.sohu.com'):
                links.remove(link)
            link = 'http:%s' %link
            request = Request(link, callback=self.parse_sohu)
            request.meta['link'] = link
            yield request

    def parse_sohu(self, response):
        item = SohuItem()
        response = response.replace(body=filter(response.body))
        url = response.meta['link']
        title = response.xpath('//*[@id="article-container"]/div[2]/div[1]/div[1]/h1[1]/text()').extract()
        title.remove(title[1])
        tags = response.xpath('//*[@id="article-container"]/div[2]/div[1]/div[1]/div/span[3]/a/text()').extract()
        tag = ','.join(tags)
        time = response.xpath('//*[@id="news-time"]/text()').extract()
        source = response.xpath('//*[@id="user-info"]/h4/a/text()').extract()
        sourcetype = response.xpath('/html/body/div[1]/div[1]/a/text()').extract()
        contents = response.xpath('//*[@id="article-container"]/div[2]/div[1]').extract()
        content = ','.join(contents)
        pattern = '<div class="text-title">.*?</div>'
        new_content = re.sub(pattern, ' ', content)
        item['Url'] = url
        item['Title'] = title[0]
        item['SourceType'] = sourcetype[0]
        item['Keywords'] = tag
        item['PublishTime'] = time[0]
        item['Source'] = "搜狐"
        item['Content'] =new_content
        item['Author'] = source[0]
        item['Favorites'] = 0
        item['ReadCounts'] = 0
        item['Status'] = 0
        item['Category_ID'] = 0
        item['Source_ID'] = 27
        yield item

