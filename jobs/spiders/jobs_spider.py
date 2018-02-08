# -*- coding: utf-8 -*-
import scrapy
import time
from jobs.items import JobsItem


class jobs_spider(scrapy.Spider):
    # name use for "srapy crawl name"
    name = 'jobs'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['http://www.zhipin.com/']

    # query para
    positionUrl = 'http://www.zhipin.com/c101280600/h_101280600/?query=python'
    curPage = 1


    # disguised as a browser
    headers = {
        'x-devtools-emulate-network-conditions-client-id': "5f2fc4da-c727-43c0-aad4-37fce8e3ff39",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'dnt': "1",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
        'cookie': "__c=1501326829; lastCity=101020100; __g=-; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.20.1.20.20; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502948718; __c=1501326829; lastCity=101020100; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502954829; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.21.1.21.21",
        'cache-control': "no-cache",
        'postman-token': "76554687-c4df-0c17-7cc0-5bf3845c9831"
    }

    # return iterable
    def start_requests(self):
        return [self.next_request()]

    # handle response data and return format data
    def parse(self, response):
        print("request -> " + response.url)
        job_list = response.css('div.job-list > ul > li')
        for job in job_list:
            item = JobsItem()
            job_primary = job.css('div.job-primary')
            # item['pid'] = job.css('div.info-primary > h3 > a::attr(data-jobid)').extract_first().strip()
            item["job_title"] = job_primary.css('div.info-primary > h3 > a::text').extract_first().strip()
            item["job_salary"] = job_primary.css('div.info-primary > h3 > a > span::text').extract_first().strip()
            info_primary = job_primary.css('div.info-primary > p::text').extract()
            item['job_addr'] = info_primary[0].strip()
            item['job_exp'] = info_primary[1].strip()
            item['job_edu'] = info_primary[2].strip()
            item['company_name'] = job_primary.css(
                'div.info-company > div.company-text > h3 > a::text').extract_first().strip()
            company_infos = job_primary.css('div.info-company > div.company-text > p::text').extract()
            if len(company_infos) == 3:  # 有一条招聘这里只有两项，所以加个判断
                item['company_type'] = company_infos[0].strip()
                # item['financeStage'] = company_infos[1].strip()
                item['company_employee_num'] = company_infos[2].strip()
                item['job_tags'] = job.css('li > div.job-tags > span::text').extract()
                # item['time'] = job.css('span.time::text').extract_first().strip()
                # item['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            yield item
        self.curPage += 1
        time.sleep(5)

        # send response
        yield self.next_request()

    def next_request(self):
        # scrapy.http.FormRequest(url=u(page%d % (page) ), headers=h, callback=c)
        return scrapy.http.FormRequest(self.positionUrl + ("&page=%d&ka=page-%d" % (self.curPage, self.curPage)),
                                       headers=self.headers, callback=self.parse)
