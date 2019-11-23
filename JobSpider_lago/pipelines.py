# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter

# 导入setting是配置信息
from JobSpider_lago.settings import *
import pymysql
import json


# 最开始的pipeline
class JobspiderLagoPipelineDefault(object):

    def process_item(self, item, spider):
        return item


class JobspiderLagoPipelineMySql(object):

    # 初始化MySQL连接操作
    def open_spider(self, spider):

        # 使用settings的配置连接MySQL
        self.db = pymysql.connect(host=MYSQLHOST, user=MYSQLUSER, password=MYSQLPASSWORD, db=MYSQLDATABASE,
                                  port=MYSQLPORT, charset='utf8')
        self.cu = self.db.cursor()

    def process_item(self, item, spider):
        # 判断是否是需要存储到MySQL的数据
        if item['pipelineType'] != 'mysql':
            return item

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
            # 将数据插入MySQL
            self.cu.execute(
                'insert into jobInfo( '
                'keyword, city, companyLabelList, companySize, financeStage, firstType, jobNature,'
                'positionAdvantage, positionLables, positionName, salary, secondType, thirdType, workYear'
                ')values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                data
            )
        except Exception as e:
            print(e)
            # 插入数据失败回滚操作
            self.db.rollback()
        else:
            # 插入数据成功提交数据
            self.db.commit()
        return item

    # 关闭MySQL连接
    def close_spider(self, spider):
        self.cu.close()
        self.db.close()


class JobspiderLagoPipelineJson(object):

    # 初始化Json文件写入连接操作
    def open_spider(self, spider):
        # 创建一个json文件写入对象
        self.exportJson = JsonItemExporter(file=open('./dataDir/dataJson.json', 'wb'), encoding='utf-8',
                                           ensure_ascii=False)

        # 开启json数据导出初始化
        self.exportJson.start_exporting()

    # 关闭Json文件连接
    def close_spider(self, spider):
        self.exportJson.finish_exporting()

    # 写入item的json数据数据
    def process_item(self, item, spider):
        if item['pipelineType'] != 'json':
            return item

        # 写入json数据
        self.exportJson.export_item(item)

        return item


