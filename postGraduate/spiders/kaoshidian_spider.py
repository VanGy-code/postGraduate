# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import lxml


class KaoshidianSpiderSpider(CrawlSpider):
    name = 'kaoshidian_spider'
    allowed_domains = ['www.kaoshidian.com']
    start_urls = ['http://www.kaoshidian.com/kaoyan/school']

    rules = (
        # 跟进每一个学校的详细界面
        Rule(LinkExtractor(allow=r'/kaoyan/school/.*/.html', restrict_xpaths='//div[@class="main"]//div[contains('
                                                                             '@class,"list_data")]//dd//div[contains('
                                                                             '@class,"c0")]//a/@href'),
             callback='parse_item', follow=True),
    )
    
    # def parse_start_url(self, response):
    #    pass
        
    def parse_item(self, response):
        #item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        #return item
        pass
        