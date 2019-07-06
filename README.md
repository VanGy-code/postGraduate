
# Scrapy for information of postgraduate college(Scrapy通用爬虫爬取国内考研信息资讯)

![language](https://img.shields.io/badge/language-Python-blue.svg)
![platform](https://img.shields.io/badge/platform-ios|Linux|Windows-lightgrey.svg)
[![codebeat badge](https://codebeat.co/badges/f56ff221-9a8f-4bc2-bfa3-6885ea07bf4f)](https://codebeat.co/projects/github-com-colordoge-postgraduate-master) ![GitHub repo size](https://img.shields.io/github/repo-size/ColorDoge/postGraduate.svg) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Scrapy.svg)

<!-- TOC -->

- [Scrapy for information of postgraduate college(Scrapy通用爬虫爬取国内考研资讯)](#Scrapy-for-information-of-postgraduate-collegeScrapy%E9%80%9A%E7%94%A8%E7%88%AC%E8%99%AB%E7%88%AC%E5%8F%96%E5%9B%BD%E5%86%85%E8%80%83%E7%A0%94%E8%B5%84%E8%AE%AF)
  - [一、项目目标](#%E4%B8%80%E9%A1%B9%E7%9B%AE%E7%9B%AE%E6%A0%87)
  - [二、编译环境](#%E4%BA%8C%E7%BC%96%E8%AF%91%E7%8E%AF%E5%A2%83)
  - [三、使用技术介绍](#%E4%B8%89%E4%BD%BF%E7%94%A8%E6%8A%80%E6%9C%AF%E4%BB%8B%E7%BB%8D)
  - [四、爬取思路](#%E5%9B%9B%E7%88%AC%E5%8F%96%E6%80%9D%E8%B7%AF)
  - [五、爬取分析](#%E4%BA%94%E7%88%AC%E5%8F%96%E5%88%86%E6%9E%90)
  - [六、项目进度](#%E5%85%AD%E9%A1%B9%E7%9B%AE%E8%BF%9B%E5%BA%A6)
    - [（一）新建项目及项目配置](#%E4%B8%80%E6%96%B0%E5%BB%BA%E9%A1%B9%E7%9B%AE%E5%8F%8A%E9%A1%B9%E7%9B%AE%E9%85%8D%E7%BD%AE)
    - [（二）定义 Rule（获取链接的规则）](#%E4%BA%8C%E5%AE%9A%E4%B9%89-Rule%E8%8E%B7%E5%8F%96%E9%93%BE%E6%8E%A5%E7%9A%84%E8%A7%84%E5%88%99)
    - [（三）解析页面（数据提取)](#%E4%B8%89%E8%A7%A3%E6%9E%90%E9%A1%B5%E9%9D%A2%E6%95%B0%E6%8D%AE%E6%8F%90%E5%8F%96)
    - [（四）数据清洗](#%E5%9B%9B%E6%95%B0%E6%8D%AE%E6%B8%85%E6%B4%97)
    - [（五）通用配置抽取](#%E4%BA%94%E9%80%9A%E7%94%A8%E9%85%8D%E7%BD%AE%E6%8A%BD%E5%8F%96)
    - [（六）数据存储](#%E5%85%AD%E6%95%B0%E6%8D%AE%E5%AD%98%E5%82%A8)
  - [七、使用说明](#%E4%B8%83%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)

<!-- /TOC -->

## 一、项目目标

___

&emsp;&emsp;本项目的主要目标是爬取[中国研究生招生信息网](https://yz.chsi.com.cn)的信息库。其中包括院校信息的院校简介、下属学院设置、招生政策布、网上报考公告以及调剂政策。专业信息包括，专业所属科目、专业门目、专业代码称。

&emsp;&emsp;其次，通过爬去其他提供可靠研究生招生信息的网站，如[考试点](http://m.kaoshidian/.eb)，加以对比和筛选数据，增强数据可靠性。

## 二、编译环境以及准备工作

___

1.python

2.Scrapy 框架
&emsp;&emsp;Scrapy 是一个基于 Twisted 的异步处理框架， 是纯 Python 实现的爬虫框架， 其架构清晰， 榄块之 间的榈合程度低， 可扩展性极强， 可以灵活完成各种需求 。 我们只需要定制开发几个模块就可以轻松 实现一个爬虫。
3.Splash
4.MySQL
  
  
## 三、使用技术介绍

___

## 四、爬取思路

___

&emsp;&emsp;我们需要大规模爬取研招网的院校库以及专业库的信息。
&emsp;&emsp;以研招网首页为起点，爬取信息库中的院校库和专业库中的信息。院校库中采用的爬取方法是，以院校库列表为起点爬取爬取各大院校在研招网的信息主页，再由各大院校在研招网的信息主页爬取各大院校的院校简介、招生简章、信息发布、网报公告、调剂政策，依次类推，递归爬取院校信息。
&emsp;&emsp;专业库相对院校库较特殊，专业列表是通过JavaScript加载的，所以需要Splash 执行页面渲染。这里采用的爬取策略是， 利用Splash 先将页面渲染返回给Scrapy，在获取到学位类型后，将学位类型的Id以post的形式发送给网站，返回该学位下设学科的信息，再通过将学科id以post形式发送给网站，返回该学科下设门类信息，同理，将门类id以post形式发送给网站即可获得该门类下设所以学科的信息。依次类推，递归爬取专业信息

## 五、爬取分析

___


## 六、项目进度

___

### （一）新建项目及项目配置

___

- [x] 创建Scrapy爬虫项目文件
- [x] git 链接🔗github 远程代码仓库
  ___
- [x] 创建[统用爬虫](https://github.com/ColorDoge/postGraduate/blob/master/postGraduate/spiders/kaoYan.py)
- [x] 创建[研招网数据爬虫](https://github.com/ColorDoge/postGraduate/blob/master/postGraduate/spiders/yanzhaowang_spider.py)
- [x] 创建[考试点数据爬虫](https://github.com/ColorDoge/postGraduate/blob/master/postGraduate/spiders/kaoshidian_spider.py)

  ___

- [x] 设置[用户头信息（RandomUserAgentMiddleware）](https://github.com/ColorDoge/postGraduate/blob/master/postGraduate/middlewares.py)
- [x] Scrapy对接Splash渲染网页

### （二）定义 Rule（获取链接的规则）

___

1.研招网院校库链接筛选规则:

- [x] 院校库链接筛选规则
- [x] 院校信息页面链接筛选规则
- [x] 院校库列表翻页链接筛选规则
- [x] 院校信息页院校简介链接筛选规则
- [x] 招生政策列表链接筛选规则
- [x] 招生政策详情页链接筛选规则
- [x] 网报公告详情页链接筛选规则
- [x] 信息发布列表页链接筛选规则
- [x] 信息发布详情页链接筛选规则
- [x] 调剂办法列表页链接筛选规则
- [x] 调剂办法详情页链接筛选规则

  ___
  
2.研招网专业库链接筛选规则:

- [x] 专业库链接筛选规则
- [x] 专业库专业详情页链接筛选规则

### （三）解析页面（数据提取)  

___

1.院校库页面数据提取：

- [x] 使用BeautifulSoup，提取院校库列表中院校基本信息
- [x] 使用BeautifulSoup，提取院校简介详情
- [x] 使用BeautifulSoup，提取招生政策详情
- [x] 使用BeautifulSoup，提取网报公告详情
- [x] 使用BeautifulSoup，提取调剂办法详情
  ___
2.专业库页面数据提取：

- [x] 使用BeautifulSoup，提取 门类/类别
- [x] 使用Selector，提取 学科/类别
- [x] 使用Selector，提取专业信息、专业开设院校
  
### （四）数据清洗

___

&emsp;&emsp;直接从页面上获取的数据中，除了我吗需要的信息之外还存在一些因网页编写或者信息输入时发生错误所导致的字符异常以及一些转义字符。为了保持数据的有效性，我们用re库对字符串进行数据清洗.

- [x] 使用re.sub()，清洗院校基本信息
- [x] 使用re.sub()，清洗专业信息

### （五）通用配置抽取

___

### （六）数据存储

___

1. 数据库建表

  - [ ] 建立MySQL 数据库
  - [ ] 插入基本表
  
2. 使用Item Pipeline存储到MySQL:

- [ ] MysqlPipeline功能实现

## 七、使用说明

___
