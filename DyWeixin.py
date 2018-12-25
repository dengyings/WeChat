# coding: utf-8
import requests
import re 


class DyWeixin(object):
    def __init__(self,
                 official_cookie=None,
                 token=None,
                 appmsg_token=None,
                 wechat_cookie=None
                 ):

        self.officical = Arturls(cookie=official_cookie, token=token)
        self.appmsg_token, self.cookie = appmsg_token, wechat_cookie
        self.wechat = ArtInfo(self.cookie)

    def complete_info(self, nickname, begin=0, count=5):
        artiacle_data = self.officical.articles(
            nickname, begin=str(begin), count=str(count))
        for data in artiacle_data:
            article_url = data["link"]
            comments = self.wechat.comments(article_url)
            data["comments"] = comments
        return artiacle_data

class ArtInfo(object):
    '''获取文章评论'''

    def __init__(self, cookie):
        self.s = requests.session()
        #self.appmsg_token = appmsg_token
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.901.400 QQBrowser/9.0.2524.400",
            "Cookie":cookie
        }


    def comments(self, article_url):
        __biz, mid, idx, sn = self.__get_params(article_url)
        getcomment_url = "https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&__biz={}&idx={}&comment_id={}&limit=100"
        try:
            url = getcomment_url.format(__biz, idx, self.__get_comment_id(article_url))
            comment_json = self.s.get(url, headers=self.headers).json()
        except Exception as e:
            comment_json = {}
        return comment_json

    def __get_comment_id(self, article_url):
        res = self.s.get(article_url)
        comment_id = re.findall(r'comment_id = "\d+"',
                                res.text)[0].split(" ")[-1][1:-1]
        return comment_id

    def __get_params(self, article_url):
        string_lst = article_url.split("?")[1].split("&")
        dict_value = [string[string.index("=") + 1:] for string in string_lst]
        __biz, mid, idx, sn, *_ = dict_value
        sn = sn[:-3] if sn[-3] == "#" else sn       
        return __biz, mid, idx, sn


class Arturls(object):
    """
    获取需要爬取的微信公众号文章链接
    """

    def __init__(self, cookie=None, token=None):
        self.s = requests.session()
        self.headers = {
            "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0"
        }
        self.params = {
            "lang": "zh_CN",
            "f": "json",
        }

        self.headers["Cookie"] = cookie
        self.params["token"] = token

    def official_info(self, nickname, begin=0, count=5):
        """
         获取公众号的一些信息
         
        """
        search_url = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
        params = {
            "query": nickname,
            "count": str(count),
            "action": "search_biz",
            "ajax": "1",
            "begin": str(begin)
        }
        self.params.update(params)

        try:
            official = self.s.get(
                search_url, headers=self.headers, params=self.params)
            return official.json()["list"][0]
        except Exception:
            raise Exception(u"公众号名称错误或cookie、token错误，请重新输入")


    def articles(self, nickname, begin=0, count=5, type_="9", action="list_ex", query=None):
        """
        获取公众号文章的一些信息
        
        """
        appmsg_url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

        try:
            # 获取公众号的fakeid
            official_info = self.official_info(nickname)
            self.params["fakeid"] = official_info["fakeid"]
        except Exception:
            raise Exception(u"公众号名称错误或cookie、token错误，请重新输入")

        # 增加/更改请求参数
        params = {
            "query": None,
            "begin": str(begin),
            "count": str(count),
            "type": str(type_),
            "action": action
        }
        self.params.update(params)

        data = self.s.get(appmsg_url, headers=self.headers, params=self.params)
        return data.json()["app_msg_list"]