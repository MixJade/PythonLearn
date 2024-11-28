import requests
from lxml import etree
url = "https://www.shanghairanking.cn/api/pub/v1/bcur?bcur_type=11&year=2020）"
ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
AppleWebKit/537.36 (KHTML, like Gecko) \\Chrome/86.0.4240.198 Safari/537.36"'}
res = requests.get(url, headers=ua).text
html_dom = etree.HTML(res)
html = requests.get(url, headers=ua).content

with open('../../A2兼收并蓄/0514.txt', 'wb') as f:
    f.write(html)
