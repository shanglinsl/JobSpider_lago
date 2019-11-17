# -*- coding: utf-8 -*-
import scrapy
import re
import json
from JobSpider_lago.items import JobspiderLagoItem
from scrapy_redis.spiders import RedisSpider


class LagospiderSpider(scrapy.Spider):
    name = 'LagoSpider'
    # allowed_domains = ['www.lagou.com']

    def start_requests(self):
        url = 'https://www.lagou.com/jobs/list_%E5%A4%A7%E6%95%B0%E6%8D%AE/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        yield scrapy.FormRequest(
            url=url,
            headers=headers,
            callback=self.get_listJob,
            dont_filter=True
        )

    def get_listJob(self, response):
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
            break

    def getJobInfo(self, response):
        sid = response.meta['sid']
        jsonJobData = json.loads(response.text)
        result = jsonJobData['content']['positionResult']['result']
        for job in result:
            positionId = job['positionId']
            url = 'https://www.lagou.com/jobs/{}.html?show=79a9491071e94813ae6e954c7e7ea77e'.format(positionId)
            keyword = jsonJobData['content']['positionResult']['queryAnalysisInfo']['positionName']
            yield scrapy.FormRequest(
                url=url,
                meta={
                    'keyword': keyword,
                    'job': job
                },
                dont_filter=True,
                callback=self.parse
            )

    def parse(self, response):
        keyword = response.meta['keyword']
        item = JobspiderLagoItem()

        job = response.meta['job']

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

        item['keyword'] = keyword
        item['jobData'] = jobData

        yield item
