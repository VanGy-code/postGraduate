# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

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
    collegeLeaderInfo = scrapy.Field
    collegeIntro = scrapy.Field()
    surrounding = scrapy.Field()


class enrollmentGuideIndexItem(scrapy.Item):
    collection = table = 'EnrollmentGuideIndex'
    collegeName = scrapy.Field()
    # num = scrapy.Field()
    title = scrapy.Field()
    releaseTime = scrapy.Field()


class enrollmentGuideItem(scrapy.Item):
    collection = table = 'EnrollmentGuideAritcle'
    collegeName = scrapy.Field()
    title = scrapy.Field()
    mainBody = scrapy.Field()


class moreInfoIndexItem(scrapy.Item):
    collection = table = 'moreInfoIndex'
    collegeName = scrapy.Field()
    # num = scrapy.Field()
    title = scrapy.Field()
    releaseTime = scrapy.Field()


class moreInfoItem(scrapy.Item):
    collection = table = 'moreInfo'
    collegeName = scrapy.Field()
    title = scrapy.Field()
    mainBody = scrapy.Field()


class onlineRegistrationAnnouncementItem(scrapy.Item):
    collection = table = 'onlineRegistrationAnnouncement'
    collegeName = scrapy.Field()
    title = scrapy.Field()
    mainBody = scrapy.Field()


class adjustMethodIndexItem(scrapy.Item):
    collection = table = 'adjustMethodIndex'
    collegeName = scrapy.Field()
    # num = scrapy.Field()
    title = scrapy.Field()
    releaseTime = scrapy.Field()


class adjustMethodItem(scrapy.Item):
    collection = table = 'adjustMethod'
    collegeName = scrapy.Field()
    title = scrapy.Field()
    mainBody = scrapy.Field()


class degreeItem(scrapy.Item):
    collection = table = 'degree'
    id = scrapy.Field()
    name = scrapy.Field()


class fieldItem(scrapy.Item):
    collection = table = 'field'
    id = scrapy.Field()
    name = scrapy.Field()
    degreeId = scrapy.Field()


class subjectItem(scrapy.Item):
    collection = table = 'subject'
    id = scrapy.Field()
    name = scrapy.Field()
    fieldId = scrapy.Field()


class majorItem(scrapy.Item):
    collection = table = 'major'
    id = scrapy.Field()
    name = scrapy.Field()
    subjectId = scrapy.Field()


class majorCollegeItem(scrapy.Item):
    collection = table = 'majorCollege'
    code = scrapy.Field()
    name = scrapy.Field()
    college = scrapy.Field()


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