该爬虫使用scrapy框架,爬取汽车之家带标签的数据,比如:https://k.autohome.com.cn/spec/31523/ 链接下的数据。
setting中需要设置阿布云代理以及mysql和mongo地址.
mysql用来获取specId,mongo用来保存数据。