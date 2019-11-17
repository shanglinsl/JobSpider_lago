# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
import re
import json
import time

class LagospiderRedisspiderSpider(RedisSpider):
    name = 'LagoSpider_redisSpider'
    allowed_domains = ['www.lagou.com']
    # start_urls = ['http://www.lagou.com/']
    # lpush lago_redisSpiderUrlsKeys:start_urls https://www.lagou.com/jobs/list_%E5%A4%A7%E6%95%B0%E6%8D%AE/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput=
    redis_key = 'lago_redisSpiderUrlsKeys:start_urls'

    def __init__(self):
        print("redisSpidr init---------------")
        pass

    def closed(self, spider):
        print("redisSpidr closed---------------")
        pass

    def parse(self, response):
        totalNum = int(re.findall(r'<span class="span totalNum">(.*?)</span>', response.text, re.S)[0])

        jobDataUrl = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        for i in range(0, totalNum):
            data = {
                'first': 'false',
                'pn': str(i + 1),
                'kd': '大数据',
                'sid': '16c6a03fbc0c4db48dbb3eecff390220'
            }
            sid = '16c6a03fbc0c4db48dbb3eecff390220'

            yield scrapy.FormRequest(
                url=jobDataUrl,
                headers=headers,
                formdata=data,
                meta={'sid': sid},
                dont_filter=True,
                callback=self.getJobInfo
            )
            time.sleep(2)

    def getJobInfo(self, response):
        jsonJobData = json.loads(response.text)
        for job in jsonJobData['content']['positionResult']['result']:
            jobData = {}
            jobData['所在城市'] = job['city']
            jobData['公司氛围'] = ','.join(job['companyLabelList'])
            jobData['公司规模'] = job['companySize']
            jobData['是否上市'] = job['financeStage']
            jobData['第一工作分类'] = job['firstType']
            jobData['工作性质'] = job['jobNature']
            jobData['工作优势'] = job['positionAdvantage']
            jobData['工作技能要求'] = ','.join(job['positionLables'])
            jobData['工作名称'] = job['positionName']
            jobData['工资'] = job['salary']
            jobData['第二工作分类'] = job['secondType']
            jobData['第三工作分类'] = job['thirdType']
            jobData['工作年限要求'] = job['workYear']
            yield jobData
