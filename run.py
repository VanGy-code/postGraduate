# -*- coding: utf-8 -*-

# @Time    : 2019/5/5 18:29
# @Author  : ColorDodge
# @Email   : m18968957166@163.com
# @File    : run.py
# @Software: PyCharm

#       ___           ___           ___       ___           ___
#      /\  \         /\  \         /\__\     /\  \         /\  \
#     /::\  \       /::\  \       /:/  /    /::\  \       /::\  \
#    /:/\:\  \     /:/\:\  \     /:/  /    /:/\:\  \     /:/\:\  \
#   /:/  \:\  \   /:/  \:\  \   /:/  /    /:/  \:\  \   /::\~\:\  \
#  /:/__/ \:\__\ /:/__/ \:\__\ /:/__/    /:/__/ \:\__\ /:/\:\ \:\__\
#  \:\  \  \/__/ \:\  \ /:/  / \:\  \    \:\  \ /:/  / \/_|::\/:/  /
#   \:\  \        \:\  /:/  /   \:\  \    \:\  /:/  /     |:|::/  /
#    \:\  \        \:\/:/  /     \:\  \    \:\/:/  /      |:|\/__/
#     \:\__\        \::/  /       \:\__\    \::/  /       |:|  |
#      \/__/         \/__/         \/__/     \/__/         \|__|
#       ___           ___           ___           ___           ___
#      /\  \         /\  \         /\  \         /\  \         /\  \
#     /::\  \       /::\  \       /::\  \       /::\  \       /::\  \
#    /:/\:\  \     /:/\:\  \     /:/\:\  \     /:/\:\  \     /:/\:\  \
#   /:/  \:\__\   /:/  \:\  \   /:/  \:\__\   /:/  \:\  \   /::\~\:\  \
#  /:/__/ \:|__| /:/__/ \:\__\ /:/__/ \:|__| /:/__/_\:\__\ /:/\:\ \:\__\
#  \:\  \ /:/  / \:\  \ /:/  / \:\  \ /:/  / \:\  /\ \/__/ \:\~\:\ \/__/
#   \:\  /:/  /   \:\  /:/  /   \:\  /:/  /   \:\ \:\__\    \:\ \:\__\
#    \:\/:/  /     \:\/:/  /     \:\/:/  /     \:\/:/  /     \:\ \/__/
#     \::/__/       \::/  /       \::/__/       \::/  /       \:\__\
#      ~~            \/__/         ~~            \/__/         \/__/

import sys
from scrapy.utils.project import get_project_settings
from postGraduate.spiders.kaoshidian_spider import KaoshidianSpiderSpider
from postGraduate.utils import get_config
from scrapy.crawler import CrawlerProcess


def run():
    name = sys.argv[1]
    custom_settings = get_config(name)
    # 爬取使用的Spider名称
    spider = custom_settings.get('KaoshidianSpiderSpider')
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    # 合并配置
    settings.update(custom_settings.get('settings'))
    process = CrawlerProcess(settings)
    # 启动爬虫
    process.crawl(spider, **{'name': name})
    process.start()


if __name__ == '__main__':
    run()