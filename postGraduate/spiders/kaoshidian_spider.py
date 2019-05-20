# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from postGraduate.items import kaoshidianItem
from bs4 import BeautifulSoup
import lxml
import re


class KaoshidianSpiderSpider(CrawlSpider):
    name = 'kaoshidian_spider'
    allowed_domains = ['www.kaoshidian.com']
    start_urls = ['http://www.kaoshidian.com/kaoyan/yx-0-0-0-0-1.html']

    rules = (
        # 跟进每一个学校的详细界面
        Rule(LinkExtractor(allow=r'/kaoyan/school\/.*\.html', restrict_xpaths='//div[@class="main"]//div[contains(@class,"list_data")]//dd//a[contains(@class,"green")]'),
             callback='parse_item', follow=True),
        # <a href="http://www.kaoshidian.com/kaoyan/yx-0-0-0-0-2.html">下一页</a>
        #Rule(LinkExtractor(allow=r'/kaoyan\/.*\.html',restrict_xpaths='//div[@class="pageblk"]//div[@class="l"]//span[contains(.,"下一页")]'))
    )
    
    # def parse_start_url(self, response):
    #    pass
        
    def parse_item(self, response):
        #item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        #return item
        soup = BeautifulSoup(response.body, "lxml")
        item = kaoshidianItem()
        
        #contents = soup.find("div", attrs={"class":"main"})
        
        #self.logger.debug(contents)
        
        contents = soup.find("div",attrs={"class":"gx_intro"})
    
        
        resource = contents.find("div", attrs={"class": "right"})
        
        item["Institution"] = resource.find("h3",attrs={"class": "font_bd"}).text
        
        other_info = resource.findAll("p")
        
        location = other_info[0].find("span",attrs={"class":"sec"}).text
        location = re.sub('所属省份：', '', location)
        item["location"] = location
        
        
        collegeType = other_info[1].find("span",attrs={"class":"sec"}).text
        collegeType = re.sub('院校类型：','',collegeType)
        item["collegeType"] = collegeType
        
        natureOfCollege = other_info[1].find("span",attrs={"class":"thr"}).text
        natureOfCollege = re.sub('院校性质：','',natureOfCollege)
        item["natureOfCollege"] = natureOfCollege
        
        collegeRank = other_info[2].find("span",attrs={"class":"sec"}).text
        collegeRank = re.sub(' ','',collegeRank)
        collegeRank = re.sub('院校排名：','',collegeRank)
        item["collegeRank"] = collegeRank
        
        collegeAttrs = other_info[2].find("span",attrs={"class":"thr"}).text
        collegeAttrs = re.sub('院校属性：','',collegeAttrs)
        collegeAttrs = re.sub('\t\t\t\t\t\t\t\t\t\t\t\t','',collegeAttrs)
        collegeAttrs = re.sub('\r\n\t\t\t\t\t','',collegeAttrs)
        item["collegeAttrs"] = collegeAttrs
        
        areaCompetition = other_info[3].find("span",attrs={"class":"four"}).text
        areaCompetition = re.sub('考研地区竞争力排行：','',areaCompetition)
        item["areaCompetition"] = areaCompetition
        
        graduateSchoolRank = other_info[4].find("span").text
        graduateSchoolRank = re.sub("研究生院竞争力排行：","",graduateSchoolRank)
        item["graduateSchoolRank"] = graduateSchoolRank
        
        collegeInfo = contents.find("p",attrs={"class":"gx_dt"})
        collegeInfo = collegeInfo.text
        collegeInfo = re.sub("\u3000\u3000","",collegeInfo)
        #collegeInfo = re.sub("研究生院简介","",collegeAttrs)
        item["collegeInfo"] = collegeInfo
        
        #self.logger.debug(item)
        yield item