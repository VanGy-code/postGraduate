# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from postGraduate.items import yanzhaowangItem
from bs4 import BeautifulSoup
import lxml
import re


    
class YanzhaowangSpiderSpider(CrawlSpider):
    name = 'yanzhaowang_spider'
    allowed_domains = ['yz.chsi.com.cn']
    start_urls = ['https://yz.chsi.com.cn/sch/']
    base_url = 'https://yz.chsi.com.cn'

    # 所需的信息在目录页也有，就不定义Rule了
    rules = (
        # Rule(LinkExtractor(allow=r'sch/schoolInfo--schId-.*\.dhtml'),
        #      restrict_xpaths='//div[@class="yxk-table"]//table[@class="ch-table"]', callback='parse_item', follow=True),

        # next page(下一页)
        Rule(LxmlLinkExtractor(allow=r'sch/schoolInfo--schId-.*\.dhtml',
                            restrict_xpaths='//div[contains(@class,"pager-box")]'
                                           '//ul[contains(@class,"ch-page")]//li[@class="lip "]//i[@class="iconfont"]/../@href')
                                           ,callback='parse_index_url')
    )

 
    # def process_index_value(self,value):
    #     base_url = 'https://yz.chsi.com.cn'
    #     value = base_url + value
    #     if value:
    #         return value

    def parse_index_url(self, response):
        # 原本用 xpath 写得解析方法但是就是出现了一些未知的错误，所以干脆用比较熟悉的BeautifulSoup爽一点
        soup = BeautifulSoup(response.body, 'lxml')
        table = soup.find('table', attrs={"class": "ch-table"})
        table = table.find('tbody')
        table = table.findAll('tr')

        for school in table:
            item = yanzhaowangItem()
            attrs = school.findAll('td')

            # 解析出学校名
            name = attrs[0].find('a').text

            # 可能是研招网的反爬虫措施，用.text获取的文本有一些奇怪的东西
            # 这里用正则表达式整理一下
            name = re.sub('\r\n                                        ', '', name)
            name = re.sub('\r\n                                    ', '', name)

            # 将学校名写item
            item['Institution'] = name
            # 解析并将详细介绍的地址域名写入item
            item['url'] = self.base_url + attrs[0].find('a')['href']
            # 解析并将学校抵制写入item
            item['location'] = attrs[1].text
            # 解析并将学校的隶属单位写入item
            item['subjection'] = attrs[2].text

            # 解析出该校是否为985、211院校
            _type = attrs[3].findAll('span', attrs={'class': 'ch-table-tag'})
            # 若该校既不是985也不是211，_type将返回空列表
            if _type or len(_type):
                if _type[0].text == "985":
                    item['is985'] = True
                else:
                    item['is985'] = False

                if _type[1].text == "211":
                    item['is211'] = True
                else:
                    item['is211'] = False
            else:
                item['is985'] = False
                item['is211'] = False

            # 解析学校是否为研究生院，若是则写True,反之写False
            haveGraduateSchool = attrs[4].find('i')
            # 这里有一个很奇怪的字符表示学校是否为研究生院
            # 这个字符在web页面上显示为 一个对勾
            # 这里我们无法解析出这个字符的具体含义，但在观察各个节点的不同之后发现有这个勾的地方就会有i节点
            # 所以借由通过判断i节点是否存在来判断学校是否为研究生院
            if haveGraduateSchool != None:
                item['haveGraduateSchool'] = True
            else:
                item['haveGraduateSchool'] = False

            # 解释学校是否为自划线院校，各方面和上面的很想
            isSelfMarkingSchool = attrs[5].find('i')
            if isSelfMarkingSchool != None:
                item['isSelfMarkingSchool'] = True
            else:
                item['isSelfMarkingSchool'] = False
            yield item

        # 获取下一页，并添加请求
        # 鬼知道这个链接地址是藏在href里的，而且解析出来的东西需要连接之后才能生成请求，想用rule都用不了
        # 所以我开一个crawler_spider的意义何在???
        # next_page_url = self.base_url+response.xpath('//div[contains(@class,"pager-box")]//ul[contains(@class,'
        #                                                  '"ch-page")]//li[@class="lip "]//i['
        #                                                  '@class="iconfont"]/../@href').get()
        # yield scrapy.Request(next_page_url, callback=self.parse_start_url)
        
    def parse_schoolItem(self, response):
        pass

    def parse_item(self, response):
        item = {}
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        return item
