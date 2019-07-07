# -*- coding: utf-8 -*-
import re

import lxml
import scrapy
from bs4 import BeautifulSoup
from scrapy import FormRequest, Selector
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import (SplashFormRequest, SplashJsonResponse,
                           SplashRequest, SplashResponse, SplashTextResponse)

from postGraduate.items import (adjustMethodIndexItem, adjustMethodItem,
                                collegeInfoItem, degreeItem,
                                enrollmentGuideIndexItem, enrollmentGuideItem,
                                fieldItem, majorItem, majorCollegeItem,
                                onlineRegistrationAnnouncementItem,
                                subjectItem, yanzhaowangIntroItem)

"""
定义Lua脚本
"""
script = """
function main(splash, args)
    splash.images_enabled = false
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    return {
        html = splash:html()
    }
end
"""


class YanzhaowangSpiderSpider(CrawlSpider):
    name = 'yanzhaowang_spider'
    allowed_domains = ['yz.chsi.com.cn']
    start_urls = ['https://yz.chsi.com.cn']
    base_url = 'https://yz.chsi.com.cn/'
    base_major_url = 'https://yz.chsi.com.cn/zyk/specialityCategory.do'

    rules = (
        # # 院校库
        # Rule(LinkExtractor(
        #     allow=r'/sch/',
        #     restrict_xpaths='//div[contains(@class,"ch-nav-box-index")]'),
        #     follow=True),

        # # 院校信息
        # Rule(LinkExtractor(
        #     allow=r'sch/schoolInfo--schId-.*\.dhtml',
        #     restrict_xpaths='//div[@class="yxk-table"]//table[@class="ch-table"]'),
        #     follow=True),

        # # next page(下一页) follow是否跟进链接
        # Rule(LinkExtractor(allow=r'\?start=\d+', restrict_xpaths='//div[contains(@class,"pager-box")]'
        #                    '//ul[contains(@class,"ch-page")]//li[@class="lip "]//i[@class="iconfont"]/..'),
        #      callback='parse_index_url', follow=True),

        # # # 院校简介
        # Rule(LinkExtractor(
        #     allow=r"/sch/schoolInfo--schId-\d+\,categoryId-\d+\.dhtml",
        #     restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-content")]'
        #     '//ul[contains(@class,"yxk-link-list")]//a[contains(.,"院校简介")]'),
        #     callback='parse_school_info',
        #     follow=True),

        # # 更多招生简章
        # Rule(LinkExtractor(
        #     allow=r"/sch/listZszc--schId-\d+\,categoryId-\d+\.dhtml",
        #     restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-table-con")]'
        #     '//h4[contains(.,"招生简章")]//a[contains(.,"更多")]'),
        #     callback='parse_enrollment_guide_index',
        #     follow=True),

        # # 招生简章详情
        # Rule(LinkExtractor(
        #     allow=r"/sch/viewZszc--infoId-\d+\,categoryId-\d+\,schId-\d+\,mindex-\d+\.dhtml",
        #     restrict_xpaths='//div[contains(@class,"container")]//table'),
        #     callback='parse_enrollment_guide',
        #     follow=True),

        # # 更多信息发布
        # Rule(LinkExtractor(allow=r"/sch/listBulletin--schId-\d+\,categoryId-\d+\.dhtml",
        #                    restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-table-con")]'
        #                    '//h4[contains(.,"信息发布")]//a[contains(.,"更多")]'),
        #      follow=True),

        # # 网报公告
        # Rule(LinkExtractor(allow=r"/sswbgg/pages/msg_detail.jsp\?dwdm=\d+\&msg_id=\d+",
        #                    restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-table-con")]'
        #                    '//table[contains(@id,"wbggtable")]'), callback="parse_online_registration_announcement",
        #      follow=True),

        # # 更多调剂办法
        # Rule(LinkExtractor(allow=r"/sch/tjzc--method-listPub,schId-\d+\,categoryId-\d+\.dhtml",
        #                    restrict_xpaths='//div[contains(@class,"container")]//div[contains(@class,"yxk-table-con")]'
        #                    '//h4[contains(.,"调剂办法")]//a[contains(.,"更多")]'),
        #      callback='parse_adjust_method_index', follow=True),

        # # 调剂办法详情
        # Rule(LinkExtractor(
        #     allow=r"/sch/tjzc--method-viewPub,infoId-\d+\,categoryId-\d+\,schId-\d+\,mindex-\d+\.dhtml",
        #     restrict_xpaths='//div[contains(@class,"container")]//table'),
        #     callback='parse_adjust_method',
        #     follow=True),


        # 专业库
        Rule(LinkExtractor(
            allow=r"/zyk",
            restrict_xpaths='//ul[contains(@class,"nav-td")]'),
            process_request='splash_request',
            callback='parse_degree',
            follow=True),

        # 专业主页
        # Rule(LinkExtractor(
        #     allow=r"/zyk/specialityDetail.do\?zymc=(.*)&zydm=\d+\&cckey=\d+\&ssdm=&method=distribution#zyk-zyfb",
        #     restrict_xpaths='//tr'),
        #     callback='parse_test',
        #     follow=True),

    )

    """
    重写父类，包装SplashRequest
    """

    def splash_request(self, request):
        """
          process_request is a callable, or a string (in which case a method from the spider object with that name will
        be used) which will be called with every request extracted by this rule,
        and must return a request or None (to filter out the request).
        :param request:
        :return: SplashRequest
        """
        return SplashRequest(url=request.url, callback=self.parse_degree, args={'wait': 1})

    # 重写CrawlSpider 的方法
    def _requests_to_follow(self, response):
        """
        splash 返回的类型 有这几种SplashTextResponse, SplashJsonResponse, SplashResponse以及scrapy的默认返回类型HtmlResponse
        所以我们这里只需要检测这几种类型即可，相当于扩充了源码的检测类型
        :param response:
        :return:
        """
        # print(type(response)) # <class 'scrapy_splash.response.SplashTextResponse'>
        if not isinstance(response, (SplashTextResponse, SplashJsonResponse, SplashResponse, HtmlResponse)):
            return
        print('==========================进入_requests_to_follow=========================')
        seen = set()

        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)

    def _build_request(self, rule, link):
        # 重要！！！！！这里重写父类方法，特别注意，需要传递meta={'rule': rule, 'link_text': link.text}
        # 详细可以查看 CrawlSpider 的源码
        r = SplashRequest(url=link.url, callback=self._response_downloaded, meta={'rule': rule, 'link_text': link.text},
                          args={'wait': 5, 'url': link.url, 'lua_source': script})
        r.meta.update(rule=rule, link_text=link.text)
        return r

    """
    院校库信息提取方法
    """

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
                                'class': 'header-wrapper'}).find('h1', attrs={'class': 'zx-yx-title'}).find('a').text

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
                                'class': 'header-wrapper'}).find('h1', attrs={'class': 'zx-yx-title'}).find('a').text

        collegeName = re.sub('"', "", collegeName)
        collegeName = re.sub('\ue835', "", collegeName)

        contant = soup.find('div', attrs={'class': 'container'})
        articlesList = contant.find('tbody').findAll('tr')

        if len(articlesList) > 0:
            for article in articlesList:
                item = enrollmentGuideIndexItem()

                articleNum = article.findAll('td')[0].text
                articleNum = re.sub(' ', '', articleNum)
                articleNum = re.sub('\n', '', articleNum)

                enrollmentGuideTitle = article.findAll('td')[1].text
                enrollmentGuideTitle = re.sub('\n', '', enrollmentGuideTitle)
                enrollmentGuideTitle = re.sub(' ', '', enrollmentGuideTitle)

                releaseTime = article.findAll('td')[2].text
                releaseTime = re.sub('\n', '', releaseTime)
                releaseTime = re.sub(' ', '', releaseTime)

                item['articleNum'] = articleNum
                item['enrollmentGuideTitle'] = enrollmentGuideTitle
                item['releaseTime'] = releaseTime

                yield item

    def parse_enrollment_guide(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        collegeName = soup.find('div', attrs={
                                'class': 'header-wrapper'}).find('h1', attrs={'class': 'zx-yx-title'}).find('a').text
        collegeName = re.sub('"', "", collegeName)
        collegeName = re.sub('\ue835', "", collegeName)

        content = soup.find('div', attrs={'class': 'container'})

        title = content.find('h2', attrs={'class': 'yxk-big-title'}).text
        mainBody = content.find(
            'div', attrs={'class': 'yxk-news-contain'}).text

        item = enrollmentGuideItem()
        item['collegeName'] = collegeName
        item['title'] = title
        item['mainBody'] = mainBody

        yield item

    def parse_online_registration_announcement(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        item = onlineRegistrationAnnouncementItem()

        container = soup.find('div', attrs={'class': 'container'})
        titleArea = container.find('div', attrs={'class': 'article-title-box'})
        articleTitle = titleArea.find(
            'div', attrs={'class': 'article-title'}).text

        articleFrom = titleArea.find(
            'div', attrs={'class': 'article-from'}).find('span').text
        collegeName = re.findall(r"招生单位 \[(.+?)\]", articleFrom)

        mainBody = container.find(
            'div', attrs={'class': 'article-wrap'}).find('article').text

        mainBody = re.sub('<br>', '\n', mainBody)

        item['collegeName'] = collegeName
        item['title'] = articleTitle
        item['mainBody'] = mainBody

        yield item

    def parse_adjust_method_index(self, response):
        soup = BeautifulSoup(response.body, 'lxml')

        content = soup.find('div', attrs={"class": 'container'})

        collegeName = soup.find('div', attrs={
                                'class': 'header-wrapper'}).find('h1', attrs={'class': 'zx-yx-title'}).find('a').text

        collegeName = re.sub('"', "", collegeName)
        collegeName = re.sub('\ue835', "", collegeName)

        announcements = content.find('tbody').findAll('tr')

        if len(announcements) > 0:
            for announcement in announcements:
                item = adjustMethodIndexItem()

                announcementNum = announcement.findAll('td')[0].text
                announcementNum = re.sub(' ', '', announcementNum)
                announcementNum = re.sub('\n', '', announcementNum)

                announcementTitle = announcement.findAll('td')[1].text
                announcementTitle = re.sub('\n', '', announcementTitle)
                announcementTitle = re.sub(' ', '', announcementTitle)

                releaseTime = announcement.findAll('td')[2].text
                releaseTime = re.sub('\n', '', releaseTime)
                releaseTime = re.sub(' ', '', releaseTime)

                item['num'] = announcementNum
                item['title'] = announcementTitle
                item['releaseTime'] = releaseTime

                yield item

    def parse_adjust_method(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        collegeName = soup.find('div', attrs={
            'class': 'header-wrapper'}).find('h1', attrs={'class': 'zx-yx-title'}).find('a').text
        collegeName = re.sub('"', "", collegeName)
        collegeName = re.sub('\ue835', "", collegeName)

        content = soup.find('div', attrs={'class': 'container'})

        title = content.find('h2', attrs={'class': 'yxk-big-title'}).text
        mainBody = content.find(
            'div', attrs={'class': 'yxk-news-contain'}).text

        mainBody = re.sub('\xa0', '', mainBody)

        item = adjustMethodItem()
        item['collegeName'] = collegeName
        item['title'] = title
        item['mainBody'] = mainBody

        yield item

    """
    专业库信息提取方法
    """

    def parse_degree(self, response):

        soup = BeautifulSoup(response.body, 'lxml')
        container = soup.find('div', attrs={'class': 'zyk-list'})

        degreeContainer = container.find('ul', attrs={'class': 'zyk-cc-ul'})
        degreeList = degreeContainer.findAll('li')

        for degree in degreeList:
            item = degreeItem()

            degreeId = degree.attrs['id']
            degreeName = degree.text
            degreeName = re.sub('\ue6a2', '', degreeName)

            item['id'] = degreeId
            item['name'] = degreeName
            yield item

        for degree in degreeList:
            degreeId = degree.attrs['id']
            # self.logger.debug(degreeId)
            yield SplashFormRequest(self.base_major_url,
                                    formdata={'method': 'subCategoryMl',
                                              'key': degreeId},
                                    callback=self.parse_field
                                    )

    def parse_field(self, response):

        selector = Selector(text=response.body)
        fieldList = selector.xpath('//li')

        if len(fieldList):

            for field in fieldList:

                item = fieldItem()

                fieldId = field.xpath('@id').extract()[0]
                fieldName = field.xpath('./text()').extract()[0]
                fieldName = re.sub('\ue6a2', '', fieldName)

                item['id'] = fieldId
                item['name'] = fieldName
                yield item

            for field in fieldList:
                fieldId = field.xpath('@id').extract()[0]
                # self.logger.debug(degreeId)
                yield SplashFormRequest(self.base_major_url,
                                        formdata={'method': 'subCategoryMl',
                                                'key': fieldId},
                                        callback=self.parse_subject
                                        )

    def parse_subject(self, response):

        selector = Selector(text=response.body)
        subjectList = selector.xpath('//li')

        if len(subjectList):
            for subject in subjectList:
                item = subjectItem()

                subjectId = subject.xpath('@id').extract()[0]
                subjectName = subject.xpath('./text()').extract()[0]
                subjectName = re.sub('\ue6a2', '', subjectName)

                item['id'] = subjectId
                item['name'] = subjectName
                yield item

            for subject in subjectList:
                subjectId = subject.xpath('@id').extract()[0]
                yield SplashFormRequest(self.base_major_url,
                                        formdata={'method': 'subCategoryXk',
                                                'key': subjectId},
                                        callback=self.parse_major
                                        )

    def parse_major(self, response):
        selector = Selector(text=response.body)

        links = LinkExtractor(
                allow=r"/zyk/specialityDetail.do\?zymc=(.*)&zydm=\d+\&cckey=\d+\&ssdm=&method=distribution#zyk-zyfb",
                restrict_xpaths='//tr').extract_links(response)


        majorList = selector.xpath('//tr')


        majorList = majorList[1:]

        for major in majorList:
            item = majorItem()
            infoList = major.xpath('./td')

            majorId = infoList.xpath('./text()').extract()[2]
            majorId = re.sub('\n', '', majorId)
            majorId = re.sub(' ', '', majorId)

            majorName = infoList.xpath('./a/text()').extract()[0]
            majorName = re.sub('\ue6a2', '', majorName)
            majorName = re.sub('\n', '', majorName)
            majorName = re.sub(' ', '', majorName)

            item['id'] = majorId
            item['name'] = majorName
            yield item

        for link in links:
            yield scrapy.Request(link.url, callback=self.parse_test)

    def parse_test(self, response):

        soup = BeautifulSoup(response.body, 'lxml')

        majorInfo = soup.find('div',attrs={'class':'zyk-base-info'})

        self.logger.debug(majorInfo)
        if majorInfo is not None:
            majorInfo = majorInfo.text
            majorInfo = re.sub('专业名称：', '', majorInfo)
            majorInfo = re.sub('专业代码：', ',', majorInfo)
            majorInfo = re.sub('门类/类别：', ',', majorInfo)
            majorInfo = re.sub('学科/类别：', ',', majorInfo)
            majorInfo = re.sub(' ', '', majorInfo)
            majorInfo = re.sub(r'\n', '', majorInfo)
            majorInfo = re.sub('\u2002', '', majorInfo)
            majorInfo = re.sub(r'\r', '', majorInfo)
            majorList = majorInfo.split(',')


        table_container = soup.find('div', attrs={'class': 'tab-container'})
        if table_container is not None:
            collegeList = table_container.findAll('li')
            
            if len(collegeList):
                for college in collegeList:
                    item = majorCollegeItem()

                    name = college.attrs['title']

                    item['code'] = majorList[1]
                    item['name'] = name
                    item['college'] = majorList[0]

                    yield item
