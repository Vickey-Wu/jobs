# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymysql
import time


# class JobsPipeline(object):
#     def process_item(self, item, spider):
#         return item


class JobsPipeline(object):
    def process_item(self, item, spider):
        host = settings['MYSQL_HOSTS']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DB']
        c = settings['CHARSET']

        jobs_sql = '''INSERT INTO website.jobs_jobsinfo (job_title, job_salary, job_requirement, job_addr, job_exp, job_edu, job_tags, company_name, company_employee_num, company_type) VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9})'''

        # make sure the sequence is the same as sql format sequence
        jobs_list = [item['job_title'], item['job_salary'], item['job_requirement'], item['job_addr'], item['job_exp'],
                     item['job_edu'], item['job_tags'], item['company_name'],
                     item['company_employee_num'],
                     item['company_type']]

        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c)
        cur = con.cursor()

        try:
            cur.executemany(jobs_sql, jobs_list)
        except Exception as e:
            print('Insert error', e)
            con.rollback()
        else:
            con.commit()
        cur.close()
        con.close()
        return item
