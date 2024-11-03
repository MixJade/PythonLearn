import requests
from lxml import etree

url = "https://pvp.qq.com/web201605/herolist.shtml"
ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
AppleWebKit/537.36 (KHTML, like Gecko) \\Chrome/86.0.4240.198 Safari/537.36"'}
rs = requests.get(url, headers=ua)
rs.encoding = "gbk"
body = rs.text
html = etree.HTML(body)
alt01 = html.xpath("//ul[@class='herolist clearfix']/li/a/img/@alt")
print(alt01)

alt02 = html.xpath('//a[contains(@href,"herodetail/")]/@href')
shu = range(len(alt01))
zuizong = alt01
for k in shu:
    url02 = 'https://pvp.qq.com/web201605/' + alt02[k]
    # 参考地址'https://pvp.qq.com/web201605/herodetail/523.shtml'
    rs02 = requests.get(url02, headers=ua)
    rs02.encoding = "gbk"
    body02 = rs02.text
    html02 = etree.HTML(body02)
    shengcun = html02.xpath('//i[contains(@style,"width")]/@style')
    for i in range(len(shengcun)):
        shengcun[i] = shengcun[i].strip("width:")
        shengcun[i] = shengcun[i].strip("%")
        zuizong[k] = zuizong[k] + '  ,  ' + shengcun[i]

hk = '英雄名称,生存能力,攻击伤害,技能效果,上手难度\n'
for j in shu:
    hk = hk + str(zuizong[j]) + '\n'

with open("../../A2兼收并蓄/0520.txt", "w", encoding="utf-8") as f:
    f.writelines(hk)
    f.close()
