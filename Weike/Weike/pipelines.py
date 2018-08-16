# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class WeikePipeline(object):
    def process_item(self, item, spider):
        if item:
            # for data in datas:
            jsons = json.dumps(dict(item),ensure_ascii=False) + '\n'
            with open('E:\weikes.json','a+',encoding='utf-8') as f:
                    f.write(jsons)
        return item
