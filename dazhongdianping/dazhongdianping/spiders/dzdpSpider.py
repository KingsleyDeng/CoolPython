"""
    大众点评
"""
import re

import requests
import scrapy
from fontTools.ttLib import TTFont

from dazhongdianping.items import DazhongdianpingItem

'''大众点评小爬虫'''


class DZDPSpider(scrapy.Spider):
    name = 'dazhongdianping'
    allowed_domains = ['dianping.com']

    def start_requests(self):
        urls = ['http://www.dianping.com/hangzhou/ch10']
        for i in range(2, 50):
            urls.append('http://www.dianping.com/hangzhou/ch10/p' + str(i))
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        if response.url:
            # 获取三种woff文件的url地址
            url = 'https:' + response.xpath('.//link[contains(@href,"svgtextcss")]/@href').extract_first()
            tagname_woff_url, shopnum_woff_url, address_woff_url = self.getWoffUrls(url)
            # 获得对应的破解字典
            tagname_crack_dict = self.getCrackDict(tagname_woff_url, 'tagname')
            shopnum_crack_dict = self.getCrackDict(shopnum_woff_url, 'shopnum')
            address_crack_dict = self.getCrackDict(address_woff_url, 'address')
            # 提取我们想要的数据
            all_infos = re.findall(r'<li class="" >(.*?)<div class="operate J_operate Hide">', response.text,
                                   re.S | re.M)

            for info in all_infos:
                item = DazhongdianpingItem()
                # 店名
                item['shopname'] = re.findall(r'<h4>(.*?)<\/h4>', info, re.S | re.M)[0]
                # 点评数量
                try:
                    num_comments = \
                        re.findall(r'LXAnalytics\(\'moduleClick\', \'shopreview\'\).*?>(.*?)<\/b>', info, re.S | re.M)[
                            0]
                    num_comments = ''.join(re.findall(r'>(.*?)<', num_comments, re.S | re.M))
                    for k, v in shopnum_crack_dict.items():
                        num_comments = num_comments.replace(k, str(v))
                    item['num_comments'] = num_comments
                except:
                    item['num_comments'] = 'null'
                # --人均价格
                try:
                    avg_price = re.findall(r'<b>￥(.*?)<\/b>', info, re.S | re.M)[0]
                    avg_price = ''.join(re.findall(r'>(.*?)<', avg_price, re.S | re.M))
                    for k, v in shopnum_crack_dict.items():
                        avg_price = avg_price.replace(k, str(v))
                    item['avg_price'] = avg_price
                except:
                    item['avg_price'] = 'null'
                # --美食类型
                food_type = \
                    re.findall(r'<a.*?data-click-name="shop_tag_cate_click".*?>(.*?)<\/span>', info, re.S | re.M)[0]
                food_type = ''.join(re.findall(r'>(.*?)<', food_type, re.S | re.M))
                for k, v in tagname_crack_dict.items():
                    food_type = food_type.replace(k, str(v))
                item['food_type'] = food_type
                # --所在商区
                business_district_name = \
                    re.findall(r'<a.*?data-click-name="shop_tag_region_click".*?>(.*?)<\/span>', info, re.S | re.M)[0]
                business_district_name = ''.join(re.findall(r'>(.*?)<', business_district_name, re.S | re.M))
                for k, v in tagname_crack_dict.items():
                    business_district_name = business_district_name.replace(k, str(v))
                item['business_district_name'] = business_district_name
                # --具体位置
                location = re.findall(r'<span class="addr">(.*?)<\/span>', info, re.S | re.M)[0]
                location = ''.join(re.findall(r'>(.*?)<', location, re.S | re.M))
                for k, v in address_crack_dict.items():
                    location = location.replace(k, str(v))
                item['location'] = location
                # --口味评分
                try:
                    taste_score = re.findall(r'口味<b>(.*?)<\/b>', info, re.S | re.M)[0]
                    taste_score = ''.join(re.findall(r'>(.*?)<', taste_score, re.S | re.M))
                    for k, v in shopnum_crack_dict.items():
                        taste_score = taste_score.replace(k, str(v))
                    item['taste_score'] = taste_score
                except:
                    item['taste_score'] = 'null'
                # --环境评分
                try:
                    environment_score = re.findall(r'环境<b>(.*?)<\/b>', info, re.S | re.M)[0]
                    environment_score = ''.join(re.findall(r'>(.*?)<', environment_score, re.S | re.M))
                    for k, v in shopnum_crack_dict.items():
                        environment_score = environment_score.replace(k, str(v))
                    item['environment_score'] = environment_score
                except:
                    item['environment_score'] = 'null'
                # --服务评分
                try:
                    serve_score = re.findall(r'服务<b>(.*?)<\/b>', info, re.S | re.M)[0]
                    serve_score = ''.join(re.findall(r'>(.*?)<', serve_score, re.S | re.M))
                    for k, v in shopnum_crack_dict.items():
                        serve_score = serve_score.replace(k, str(v))
                    item['serve_score'] = serve_score
                except:
                    item['serve_score'] = 'null'
                # --yield
                yield item

    def getWoffUrls(self, url):
        response = requests.get(url)
        tagname_woff_url = 'https:' + re.search(r'PingFangSC-Regular-tagName.*?opentype\"\),url\(\"(.*?)woff',
                                                response.text).group(1) + 'woff'
        shopnum_woff_url = 'https:' + re.search(r'PingFangSC-Regular-shopNum.*?opentype\"\),url\(\"(.*?)woff',
                                                response.text).group(1) + 'woff'
        address_woff_url = 'https:' + re.search(r'PingFangSC-Regular-address.*?opentype\"\),url\(\"(.*?)woff',
                                                response.text).group(1) + 'woff'
        return tagname_woff_url, shopnum_woff_url, address_woff_url

    def getCrackDict(self, woff_url, fontname):
        response = requests.get(woff_url)
        with open(fontname + '.ttf', 'wb') as f:
            f.write(response.content)
        keys = TTFont(fontname + '.ttf').getGlyphOrder()
        constants = '店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下県凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才更板知己无回晚微周值费性桌拍跟块调糕'
        constants = ['', '', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0] + list(constants)
        crack_dict = {}
        for i in range(len(constants)):
            crack_dict[keys[i].replace('uni', '&#x') + ';'] = constants[i]
        return crack_dict
