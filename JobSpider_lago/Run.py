# 用于运行爬虫

from scrapy import cmdline

cmdline.execute('scrapy crawl LagoSpider'.split())
# cmdline.execute('scrapy crawl LagoSpider_redisSpider'.split())
