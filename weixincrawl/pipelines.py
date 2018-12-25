# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import pymongo
# from items import WeixincrawlItem

# class WeixincrawlPipeline(object):
    
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db


#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'weixin')
#             )

#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]

#     def close_spider(self,spider):
#         self.client.close()
            
#     def process_item(self, item, spider):
#         """ 判断item的类型，并作相应的处理，再入数据库 """
#         if isinstance(item, YunqicrawlItem):
#             try:
#                 self.db.weixinInfo.insert(dict(item))
#             except Exception:
#                 pass
#         return item
import json

class WeixincrawlPipeline(object):
    def process_item(self, item, spider):
        # 使用json的格式来写入数据到本地的文件
        with open("weixin.json", "ab") as f:
            text = json.dumps(dict(item),ensure_ascii=False)+'\n'
            f.write(text.encode('utf-8'))
        return item