import requests
import ssl
from ycTools import *
import json

class StockX():
    def __init__(self):
        self.session = requests.session()
        self.useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
        # self.session.get("https://stockx.com/zh-cn/air-jordan-6-retro-electric-green)
    def searchProductBySkucode(self, sku_code="", only_return_first=False):
        url = "https://stockx.com/api/browse?&_search={}&dataType=product".format(sku_code)
        header = headersChange("""sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"
appos: web
x-requested-with: XMLHttpRequest
sec-ch-ua-mobile: ?0
authorization: 
user-agent: {}
appversion: 0.1
accept: */*
sec-fetch-site: same-origin
sec-fetch-mode: cors
sec-fetch-dest: empty
referer: https://stockx.com/zh-cn/search?s=CT8529-003
accept-encoding: gzip, deflate
accept-language: zh-CN,zh;q=0.9,en;q=0.8""".format(self.useragent))
        res = self.session.get(url=url, headers=header, verify=False)
        if res.status_code == 200:
            try:
                res_json = json.loads(res.text)
                result = []
                for i in res_json["Products"]:
                    products = {"id": "", "sku_code": "", "urlKey": "", "title": ""}
                    products["id"] = i["id"]
                    products["sku_code"] = sku_code
                    products["urlKey"] = i["urlKey"]
                    products["title"] = i["title"]
                    products["image_url"] = i["media"]["imageUrl"]

                    result.append(products)
                return result
            except Exception as e:
                raise Exception("[error][%d]Json解析失败.." % res.status_code)
        else:
            raise Exception("[error][%d]" % res.status_code)
    def getProductInfoByUrlKey(self, urlKey="", currency="HKD"):
        url = f"https://stockx.com/api/products/{urlKey}?includes=market,360&currency={currency}&country=CN".format(urlKey=urlKey, currency=currency)
        headers = headersChange("""sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"
appos: web
x-requested-with: XMLHttpRequest
sec-ch-ua-mobile: ?0
authorization: 
user-agent: {}
appversion: 0.1
accept: */*
sec-fetch-site: same-origin
sec-fetch-mode: cors
sec-fetch-dest: empty
referer: https://stockx.com/zh-cn/air-jordan-6-retro-electric-green
accept-encoding: gzip, deflate
accept-language: zh-CN,zh;q=0.9,en;q=0.8
cookie: stockx_selected_currency=HKD;""".format(self.useragent))
        res = self.session.get(url=url, headers=headers, verify=False)
        if res.status_code == 200:
            try:
                res_json = json.loads(res.text)
                result = []
                for children_id in res_json["Product"]["children"]:
                    children = {"size": "", "retailPrice": "", "lowestAsk": ""}
                    children_obj = res_json["Product"]["children"][children_id]
                    children["size"] = children_obj["shoeSize"]
                    children["retailPrice"] = children_obj["retailPrice"]
                    children["lowestAsk"] = children_obj["market"]["lowestAsk"]
                    result.append(children)
                return result
            except Exception as e:
                raise Exception("[error][%d]Json解析失败, %s" % (res.status_code, e))
            pass
        else:
            raise Exception("[error][%d]" % res.status_code)
