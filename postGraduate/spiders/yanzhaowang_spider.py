# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from postGraduate.items import yanzhaowangIntroItem, collegeInfoItem, enrollmentGuideIndexItem, enrollmentGuideArticleItem
from bs4 import BeautifulSoup
import lxml
import re


class YanzhaowangSpiderSpider(CrawlSpider):
    name = 'yanzhaowang_spider'
    allowed_domains = ['yz.chsi.com.cn']
    start_urls = ['https://yz.chsi.com.cn']
    base_url = 'https://yz.chsi.com.cn/'

    rules = (
        # 院校库
        Rule(LinkExtractor(
            allow=r'/sch/',
            restrict_xpaths='//div[contains(@class,"ch-nav-box-index")]'),
             follow=True),

        # 专业库

        # 院校信息
        Rule(LinkExtractor(
            allow=r'sch/schoolInfo--schId-.*\.dhtml',
            restrict_xpaths=
            '//div[@class="yxk-table"]//table[@class="ch-table"]'),
             follow=True),

        # next page(下一页) follow是否跟进链接
        Rule(LinkExtractor(
            allow=r'\?start=\d+',
            restrict_xpaths='//div[contains(@class,"pager-box")]'
            '//ul[contains(@class,"ch-page")]//li[@class="lip "]//i[@class="iconfont"]/..'
        ),
             callback='parse_index_url',
             follow=False),

        # 院校简介
        Rule(LinkExtractor(
            allow=r"/sch/schoolInfo--schId-\d+\,categoryId-\d+\.dhtml",
            restrict_xpaths=
            '//div[contains(@class,"container")]//div[contains(@class,"yxk-content")]'
            '//ul[contains(@class,"yxk-link-list")]//a[contains(.,"院校简介")]'),
             callback='parse_school_info',
             follow=True),

        # 院校设置
        # Rule(LinkExtractor(allow=r"/sch/schoolInfo--schId-\d+\,categoryId-\d+\.dhtml",
        #                     restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-content")]'
        #                     '//ul[contains(@class,"yxk-link-list")]//a[contains(.,"院校设置")]'),
        #                     callback='parse_school_settings',follow=False),

        # # 专业介绍
        # Rule(LinkExtractor(allow=r"/sch/listYzZyjs--schId-\d+\,categoryId-\d+\.dhtml",
        #                    restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-content")]'
        #                     '//ul[contains(@class,"yxk-link-list")]//a[contains(.,"专业介绍")]'),
        #                     callback='parse_specialty_info',follow=False
        #                     ),

        # 录取规则
        # Rule(LinkExtractor(allow=r"/sch/schoolInfo--schId-\d+\,categoryId-\d+\.dhtml",
        #                     restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-content")]'
        #                     '//ul[contains(@class,"yxk-link-list")]//a[contains(.,"录取规则")]'),
        #                     callback='parse_admission_rules',follow=False),

        # 调剂政策
        # Rule(LinkExtractor(allow=r"/sch/schoolInfo--schId-\d+\,categoryId-\d+\.dhtml",
        #                     '//ul[contains(@class,"yxk-link-list")]//a[contains(.,"调剂政策")]'),
        #                     callback='parse_adjust_policy',follow=False),

        # 更多招生简章
        Rule(LinkExtractor(
            allow=r"/sch/listZszc--schId-\d+\,categoryId-\d+\.dhtml",
            restrict_xpaths=
            '//div[contains(@class,"container")]//div[contains(@class,"yxk-table-con")]'
            '//h4[contains(.,"招生简章")]//a[contains(.,"更多")]'),
             callback='parse_enrollment_guide_index',
             follow=False),

        # 更多信息发布
        # Rule(LinkExtractor(allow=r"/sch/listBulletin--schId-\d+\,categoryId-\d+\.dhtml",
        #                     restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-table-con")]'
        #                     '//h4[contains(.,"信息发布")]//a[contains(.,"更多")]'),follow=False),

        # 更多网报公告
        # Rule(LinkExtractor(allow=r"/sswbgg/\?dwdm=\d+\&ssdm=\d+",
        #                    restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-table-con")]'
        #                    '//h4[contains(.,"网报公告")]//a[contains(.,"更多")]'),follow=False),

        # 更多调剂办法
        # Rule(LinkExtractor(allow=r"/sch/tjzc--method-listPub,schId-\d+\,categoryId-\d+\.dhtml",
        #                    restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-table-con")]'
        #                     '//h4[contains(.,"调剂办法")]//a[contains(.,"更多")]'),follow=False),
    )

    def parse_index_url(self, response):

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
            name = re.sub('\r\n                                        ', '',
                          name)
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
        soup = BeautifulSoup(response.body, 'lxml')
        content = soup.find('div', attrs={"class": 'container'})

        collegeName = soup.find('div', attrs={
            'class': 'header-wrapper'
        }).find('h1', attrs={
            'class': 'zx-yx-title'
        }).find('a').text

        collegeName = re.sub('"', "", collegeName)
        collegeName = re.sub('\ue835', "", collegeName)

        article = content.findAll('div', attrs={'class': 'yxk-content'})

        _article = []

        for i in article:
            _article.append(i.text)

        for i in range(0, 3):
            _article[i] = re.sub('\r', '', _article[i])
            _article[i] = re.sub('\ue835', '', _article[i])
            _article[i] = re.sub('\u3000', '', _article[i])
            _article[i] = re.sub('\xa01', '', _article[i])
            _article[i] = re.sub('\xa0', '', _article[i])
            _article[i] = re.sub('\t', '', _article[i])
            _article[i] = re.sub(' ', '', _article[i])

        item = collegeInfoItem()

        item['collegeName'] = collegeName

        item['collegeLeaderInfo'] = _article[0]

        item['collegelIntro'] = _article[1]

        item['surrounding'] = _article[2]

        yield item

    def parse_enrollment_guide_index(self, response):
        soup = BeautifulSoup(response.body, 'lxml')

        collegeName = soup.find('div', attrs={
            'class': 'header-wrapper'
        }).find('h1', attrs={
            'class': 'zx-yx-title'
        }).find('a').text

        collegeName = re.sub('"', "", collegeName)
        collegeName = re.sub('\ue835', "", collegeName)

        contant = soup.find('div', attrs={'class': 'container'})
        articlesList = contant.find('tbody').findAll('tr')

        for article in articlesList:
            item = enrollmentGuideIndexItem()

            # 解析逻辑

            yield item
