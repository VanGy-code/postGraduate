# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostgraduateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 研招网简介Item
class yanzhaowangIntroItem(scrapy.Item):
    collection = table = 'Intro'
    Institution = scrapy.Field()
    location = scrapy.Field()
    subjection = scrapy.Field()
    is985 = scrapy.Field()
    is211 = scrapy.Field()
    haveGraduateSchool = scrapy.Field()
    isSelfMarkingSchool = scrapy.Field()
    url = scrapy.Field()

class collegeInfoItem(scrapy.Item):
    collection = table = 'schoolInfo'
    collegeName = scrapy.Field()
    collegeLeaderInfo = scrapy.Field()
    collegelIntro = scrapy.Field()
    surrounding = scrapy.Field()


class schoolSettingItem(scrapy.Item):
    collection = table = 'schoolSetting'
    collegeName = scrapy.Field()
    schoolName = scrapy.Field()

class specialtyInfoItem(scrapy.Item):
    collection = table = 'specialtyInfo'
    collegeName = scrapy.Field()
    specialtyName = scrapy.Field()

class admissionRuleItem(scrapy.Item):
    collection = table = 'admissionRule'
    admissionPolicy = scrapy.Field()
    crossDisciplinaryPolicy = scrapy.Field()
    
class adjustPolicyItem(scrapy.Item):
    collection = table = 'adjustPolicy'
    adjustPolicy = scrapy.Field()

class enrollmentGuideIndexItem(scrapy.Item):
    collection = table = 'EnrollmentGuideIndex'
    collegeName = scrapy.Field()
    articleNum = scrapy.Field()
    enrollmentGuideTitle = scrapy.Field()
    releaseTime = scrapy.Field()

class enrollmentGuideArticleItem(scrapy.Item):
    collection = table = 'EnrollmentGuideAritcle'
    title = scrapy.Field()
    mainBody = scrapy.Field()

# 考试点Item
class kaoshidianItem(scrapy.Item):
    collection = table = 'kaoshiwang'
    Institution = scrapy.Field()
    location = scrapy.Field()
    collegeType = scrapy.Field()
    natureOfCollege = scrapy.Field()
    collegeRank = scrapy.Field()
    collegeAttrs = scrapy.Field()
    areaCompetition = scrapy.Field()
    graduateSchoolRank = scrapy.Field()
    collegeInfo = scrapy.Field()


