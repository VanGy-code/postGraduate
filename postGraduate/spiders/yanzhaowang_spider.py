# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from postGraduate.items import yanzhaowangIntroItem
from bs4 import BeautifulSoup
import lxml
import re


    
class YanzhaowangSpiderSpider(CrawlSpider):
    name = 'yanzhaowang_spider'
    allowed_domains = ['yz.chsi.com.cn']
    start_urls = ['https://yz.chsi.com.cn/sch/']
    base_url = 'https://yz.chsi.com.cn'

    rules = (
        # 院校信息
        Rule(LinkExtractor(allow=r'sch/schoolInfo--schId-.*\.dhtml',
             restrict_xpaths='//div[@class="yxk-table"]//table[@class="ch-table"]'), callback='parse_school_item', follow=True),
       
        # next page(下一页) follow是否跟进链接
        Rule(LinkExtractor(allow=r'\?start=\d+',
                            restrict_xpaths='//div[contains(@class,"pager-box")]'
                                           '//ul[contains(@class,"ch-page")]//li[@class="lip "]//i[@class="iconfont"]/..'),
                                           callback='parse_index_url',follow=False),

        # 院校简介
        Rule(LinkExtractor(allow=r"/sch/schoolInfo--schId-\d+\,categoryId-\d+\.dhtml",
                            restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-content")]'
                            '//ul[contains(@class,"yxk-link-list")]//a[contains(.,"院校简介")]'),
                            callback='parse_school_info',follow=True),

        # 院校设置
        Rule(LinkExtractor(allow=r"/sch/schoolInfo--schId-\d+\,categoryId-\d+\.dhtml",
                            restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-content")]'
                            '//ul[contains(@class,"yxk-link-list")]//a[contains(.,"院校设置")]'),
                            callback='parse_school_settings',follow=True),

        # 专业介绍
        Rule(LinkExtractor(allow=r"/sch/listYzZyjs--schId-\d+\,categoryId-\d+\.dhtml",
                           restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-content")]'
                            '//ul[contains(@class,"yxk-link-list")]//a[contains(.,"专业介绍")]'),
                            callback='parse_department_info',follow=True
                            ),

        # 录取规则
        Rule(LinkExtractor(allow=r"/sch/schoolInfo--schId-\d+\,categoryId-\d+\.dhtml",
                            restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-content")]'
                            '//ul[contains(@class,"yxk-link-list")]//a[contains(.,"录取规则")]'),
                            callback='parse_admission_rules',follow=True),

        # 调剂政策
        Rule(LinkExtractor(allow=r"/sch/schoolInfo--schId-\d+\,categoryId-\d+\.dhtml",
                            restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-content")]'
                            '//ul[contains(@class,"yxk-link-list")]//a[contains(.,"调剂政策")]'),
                            callback='parse_adjust_policy',follow=True),
        
        # 更多招生简章
        Rule(LinkExtractor(allow=r"/sch/listZszc--schId-\d+\,categoryId-\d+\.dhtml",
                            restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-table-con")]'
                            '//h4[contains(.,"招生简章")]//a[contains(.,"更多")]'),follow=True),

        # 更多信息发布
        Rule(LinkExtractor(allow=r"/sch/listBulletin--schId-\d+\,categoryId-\d+\.dhtml",
                            restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-table-con")]'
                            '//h4[contains(.,"信息发布")]//a[contains(.,"更多")]'),follow=True),

        # 更多网报公告
        Rule(LinkExtractor(allow=r"/sswbgg/\?dwdm=\d+\&ssdm=\d+",
                           restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-table-con")]'
                           '//h4[contains(.,"网报公告")]//a[contains(.,"更多")]'),follow=True),

        # 更多调剂办法
        Rule(LinkExtractor(allow=r"/sch/tjzc--method-listPub,schId-\d+\,categoryId-\d+\.dhtml",
                           restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-table-con")]'
                            '//h4[contains(.,"调剂办法")]//a[contains(.,"更多")]'),follow=True),

    )

    def parse_start_url(self, response):
        self.parse_index_url(response)


    def parse_index_url(self, response):
        # 比较熟悉的BeautifulSoup爽一点
        soup = BeautifulSoup(response.body, 'lxml')
        table = soup.find('table', attrs={"class": "ch-table"})
        table = table.find('tbody')
        table = table.findAll('tr')

        for school in table:
            item = yanzhaowangIntroItem()
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
    

        
    def parse_school_info(self, response):
        # self.logger.debug(response.test+" 院校简介")
        pass

    def parse_school_settings(self, response):
        # self.logger.debug(response.text+" 院系设置")
        pass

    def parse_department_info(self, response):
        # self.logger.debug(" 专业介绍")
        pass
    
    def parse_adjust_policy(self, response):
        # self.logger.debug(response.text+" 调剂策略")
        pass
    
    def parse_admission_rules(self, response):
        # self.logger.debug(response.text+" 录取规则")
        pass

    def parse_more(self, response):
        self.logger.debug(response.text)

    def parse_school_item(self, response):
        pass
