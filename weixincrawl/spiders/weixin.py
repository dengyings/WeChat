# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import WeixincrawlItem
import re


class WeixinSpider(CrawlSpider):
    name = 'weixin'
    allowed_domains = ['https://mp.weixin.qq.com']


    def start_requests(self):
        url="https://mp.weixin.qq.com/cgi-bin/searchbiz",
        formdate={"query":"中原地产",
                  "count":"5",
                  "action":"search_biz",
                  "ajax":"1",
                  "begin":"0"
                  "lang":"zh_CN",
                  "f":"json"
                  "token":"621560127"}
        headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",
                 "Cookie":"rewardsn=; wxuin=1723124627; devicetype=Windows7; version=62060619; lang=zh_CN; pass_ticket=bSSOOBYMttQ3rethJqnlrF4ZhCy3grtSZOYYfVEf8qkYUQqFzi9tnGr07GGF+Rgm; wap_sid2=CJOX07UGElxSLXFSX0tZSjJueE8tRjQ2N0w0VFVsa2MzdVdKUFNCWEJtSmZta2Z6ZFZHZk5ELUpvZlBTa3Vxc0lmZWxHVlNwMWl2WGNWUzh2UHhaSWxpZjRqOWJCdHdEQUFBfjDRt+7gBTgNQAE=; wxtokenkey=777"
        }
        return [FormRequest(url=url,headers=headers,formdate=formdate,meta={'cookiejar':1},callback=self.articles)]

    def articles(self,response):
        name=response.json()["list"][0]
        fakeid=name["fakeid"]
        url="https://mp.weixin.qq.com/cgi-bin/appmsg"
        formdate = {
            "query": None,
            "begin": "0",
            "count": "5",
            "type": "9",
            "action": "list_ex"
            "fakeid":fakeid
            "lang": "zh_CN",
            "f": "json"
            "token":"621560127"
        }
        headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",
                }
        return [FormRequest(url=url,headers=headers,formdate=formdate,meta={'cookiejar':response.meta['cookiejar']},callback=self.comments)]

    def comments(self, response):
        lists = response.json()["app_msg_list"]
        for data in lists:
            url1 = data["link"]
            headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.901.400 QQBrowser/9.0.2524.400",
                     "Cookie":"rewardsn=; wxuin=1723124627; devicetype=Windows7; version=62060619; lang=zh_CN; pass_ticket=bSSOOBYMttQ3rethJqnlrF4ZhCy3grtSZOYYfVEf8qkYUQqFzi9tnGr07GGF+Rgm; wap_sid2=CJOX07UGElxSLXFSX0tZSjJueE8tRjQ2N0w0VFVsa2MzdVdKUFNCWEJtSmZta2Z6ZFZHZk5ELUpvZlBTa3Vxc0lmZWxHVlNwMWl2WGNWUzh2UHhaSWxpZjRqOWJCdHdEQUFBfjDRt+7gBTgNQAE=; wxtokenkey=777"
                    }
            res = requests.get(url=url1,headers=headers)
            comment_id = re.findall(r'comment_id = "\d+"',
                                res.text)[0].split(" ")[-1][1:-1]
            title = data["title"]
            item = WeixincrawlItem(url=url,title=title)
            url2 = "https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&__biz={}&idx={}&comment_id={}&limit=100"
            __biz, mid, idx, sn = self.__get_params(article_url)
            url = getcomment_url.format(__biz, idx, self.__get_comment_id(article_url))
            request = Request(url=url,headers=headers,callback=self.info)
            request.meta['item'] = item
            yield request

    def info(self, response):
        item = response.meta['item']
        item['Article_review'] = response.json()
        yield item


    def __get_params(self, article_url):
        string_lst = article_url.split("?")[1].split("&")
        dict_value = [string[string.index("=") + 1:] for string in string_lst]
        __biz, mid, idx, sn, *_ = dict_value
        sn = sn[:-3] if sn[-3] == "#" else sn       
        return __biz, mid, idx, sn