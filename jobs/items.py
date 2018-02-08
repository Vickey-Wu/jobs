# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field()
    job_salary = scrapy.Field()
    job_requirement = scrapy.Field()
    job_addr = scrapy.Field()
    job_exp = scrapy.Field()
    job_edu = scrapy.Field()
    job_tags = scrapy.Field()
    company_name = scrapy.Field()
    company_employee_num = scrapy.Field()
    company_type = scrapy.Field()

