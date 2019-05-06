# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class YanzhaowangSpiderSpider(CrawlSpider):
    name = 'yanzhaowang_spider'
    allowed_domains = ['yz.chsi.com.cn']
    start_urls = ['https://yz.chsi.com.cn/sch/']

    rules = (
        Rule(LinkExtractor(allow=r''), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
