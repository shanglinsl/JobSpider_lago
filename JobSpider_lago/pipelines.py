# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from JobSpider_lago.settings import *
import pymysql


# 最开始的pipeline
class JobspiderLagoPipelineDefault(object):

    def process_item(self, item, spider):
        return item


class JobspiderLagoPipelineMySql(object):

    def open_spider(self, spider):
        self.db = pymysql.connect(host=MYSQLHOST, user=MYSQLUSER, password=MYSQLPASSWORD, db=MYSQLDATABASE,
                                  port=MYSQLPORT, charset='utf8')
        self.cu = self.db.cursor()

    def process_item(self, item, spider):
        jobData = item['jobData']
        data = [
            item['keyword'],
            jobData['所在城市'],
            jobData['公司氛围'],
            jobData['公司规模'],
            jobData['是否上市'],
            jobData['第一工作分类'],
            jobData['工作性质'],
            jobData['工作优势'],
            jobData['工作技能要求'],
            jobData['工作名称'],
            jobData['工资'],
            jobData['第二工作分类'],
            jobData['第三工作分类'],
            jobData['工作年限要求']
        ]
        try:
            self.cu.execute(
                'insert into jobInfo( '
                'keyword, city, companyLabelList, companySize, financeStage, firstType, jobNature,'
                'positionAdvantage, positionLables, positionName, salary, secondType, thirdType, workYear'
                ')values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', data
            )
        except Exception as e:
            print(e)
            self.db.rollback()
        else:
            self.db.commit()

        return item

    def close_spider(self, spider):
        self.cu.close()
        self.db.close()
