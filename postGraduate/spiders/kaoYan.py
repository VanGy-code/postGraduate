# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from postGraduate.utils import get_config
from postGraduate.rules import rules


class KaoyanSpider(CrawlSpider):
    name = 'kaoYan'
    # allowed_domains = ['kaoYan']
    # start_urls = ['http://kaoYan/']
    #
    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )
    #
    # def parse_item(self, response):
    #     item = {}
    #     #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
    #     #item['name'] = response.xpath('//div[@id="name"]').get()
    #     #item['description'] = response.xpath('//div[@id="description"]').get()
    #     return item

    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        self.config = config
        self.rules = rules.get(config.get('rules'))
        self.start_urls = config.get('start_urls')
        self.allowed_domains = config.get('allowed_domains')
        super(KaoyanSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        i = {}
        return i