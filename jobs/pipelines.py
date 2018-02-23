# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymysql
import MySQLdb
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
        port = settings['MYSQL_PORT']
        charset = settings['CHARSET']
        jobs_list = []

        jobs_sql = "INSERT INTO website.jobs_jobsinfo (job_title, job_salary, job_requirement, job_addr, job_exp, job_edu, job_tags, company_name, company_employee_num, company_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # make sure the sequence is the same as sql format sequence
        jobs_list.append((item['job_title'], item['job_salary'], item['job_requirement'],
                     item['job_addr'], item['job_exp'],
                     item['job_edu'], item['job_tags'],
                     item['company_name'], item['company_employee_num'],
                     item['company_type']))

        con = MySQLdb.connect(host=host, user=user, passwd=psd, db=db, port=port)
        cur = con.cursor()

        # set charset to utf-8
        con.set_character_set('utf8')
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')

        compare_sql = 'SELECT * FROM website.jobs_jobsinfo j where company_name = "' + item['company_name'] + '"'
        r = cur.execute(compare_sql)
        print(type(r), r)
        if r:
            pass
        else:
            try:
                cur.executemany(jobs_sql, jobs_list)
                con.commit()
            except Exception as e:
                print('Insert error', e)
                # con.rollback()
            # con.commit()
            # cur.close()
            con.close()
            return item

# 
# def connect_mysql(sql, oper_type="select", data_l=None):
#     conn = pymysql.connect(host='localhost', user="root", password="123",
#                            database="website", port=3306)
#     cur = conn.cursor()
#     if oper_type == "insert":
#         cur.executemany(sql, data_l)
#         conn.commit()
#     else:
#         cur.execute(sql)
#     result = cur.fetchall()
#     conn.close()
#     return result
# 
# 
# def create_list(file_name):
#     ls = []
#     if not re.findall(file_name, r".txt"):
#         file_name += ".txt"
#     with open(file_name) as f:
#         for i in f:
#             job_title, job_salary, job_requirement, job_addr, job_exp, job_edu, job_tags, company_name, company_employee_num, company_type = i.strip().split(
#                 ",")
#             ls.append([job_title, job_salary, job_requirement, job_addr, job_exp, job_edu, job_tags, company_name, company_employee_num, company_type])
#     return ls
# 
# 
# def data_insert():
#     sql = '''INSERT INTO website.jobs_jobsinfo (job_title, job_salary, job_requirement, job_addr, job_exp, job_edu, job_tags, company_name, company_employee_num, company_type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
#     data_l = create_list("jobs_data")
#     connect_mysql(sql, oper_type="insert", data_l=data_l)
