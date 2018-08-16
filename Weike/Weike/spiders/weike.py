# -*- coding: utf-8 -*-
import scrapy
from Weike.items import WeikeItem
from Weike.txt_code import *
from Weike.settings import *
import hashlib

def hash_md5(pwd):
    h1=hashlib.md5()
    h1.update(pwd.encode('utf-8'))
    # print(h1.hexdigest())
    return h1.hexdigest()

class WeikeSpider(scrapy.Spider):
    name = 'weike'
    # allowed_domains = ['epwk.com']
    # start_urls = ['http://epwk.com/']
    # start_urls = ['https://www.epwk.com/login.html']

    # cookies = {
    #     'PHPSESSID':'3d803943a56f4f2aa5b329f7ee07418970ee0d41',
    #     'adbanner_city': '%E5%8C%97%E4%BA%AC%E5%B8%82',
    #     'UM_distinctid':'16535ff58b032f-075ce13a766465-43480420-113a00-16535ff58b1762',
    #     # 'CNZZDATA1257734387':'1782644008-1534207135-null%7C1534228767'
    # }


    def start_requests(self):
        # headers  = self.settings['DEFAULT_REQUEST_HEADERS']
        url = 'https://www.epwk.com/login.html'
        yield scrapy.Request(url=url,callback=self.login,dont_filter=True)
    # def get_code(self,response):
    #     res = scrapy.Request(url='https://www.epwk.com/secode_show.php?pre=login&sid='+str(math.radians(1)))
    #     with open('/soft/demo/secode_show1.png','wb') as f:
    #         f.write(res.content)

    def login(self,response):

        '''
        # 访问登录首页
        # :return: None
        '''
        headers = {
            'Origin': 'https://www.epwk.com',
            'Referer': 'https://www.epwk.com/login.html',
            'X-Requested-With': 'XMLHttpRequest'
        }
        DEFAULT_REQUEST_HEADERS.update(headers)

        user = self.settings['USER']
        pwd = self.settings['PWD']
        url = "https://www.epwk.com/index.php?do=login"
        data = {
            'formhash': 'f2c7b9',
            'txt_account': user,
             'pwd_password': hash_md5(pwd),
             'login_type': '3',
             'ckb_cookie': '0',
             'hdn_refer': 'http://www.epwk.com/task/index.html',
             'txt_code': txt_code(),
             'pre': 'login',
             'inajax': '1'
        }
        request =  scrapy.FormRequest(url=url,callback=self.get_page,headers=DEFAULT_REQUEST_HEADERS,formdata=data,dont_filter=True)
        yield request

    def get_page(self,response):
        base_url='http://www.epwk.com/task/page'
        for i in range(1, 1765):
            url=base_url + str(i) + '.html'
            yield scrapy.Request(url=url,callback=self.parse)


    def parse(self, response):
        # print(response)
        item = WeikeItem()
        attrs = response.xpath('//div[@class="task_class_list_li_box"]')
        for attr in attrs:
            item['url'] = attr.xpath('.//a/@url').extract_first()
            item['price']= attr.xpath('.//b/text()').extract_first()
            item['name']= attr.xpath('.//a/text()').extract_first().replace(' ', "")
            item['glance'] =  attr.xpath('.//samp/text()').extract_first().replace(' / ', '')
            item['number'] = attr.xpath('.//samp/font/text()').extract_first()
            item['finish_time'] = attr.xpath('.//span/span[1]/text()').extract_first()
            yield item


