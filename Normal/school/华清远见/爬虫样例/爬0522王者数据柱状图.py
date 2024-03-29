import requests
from lxml import etree
import pandas as pd
from pyecharts.charts import Bar

# 数据爬取
url = "https://pvp.qq.com/web201605/js/herolist.json"
ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
AppleWebKit/537.36 (KHTML, like Gecko) \\Chrome/86.0.4240.198 Safari/537.36"'}
rs = requests.get(url, headers=ua)
rs.encoding = "utf-8"
# json获取源码 返回的数据类型是列表
body = rs.json()
# 循环取出英雄名称
h = []
name = []
for i in range(len(body)):
    h.append(body[i]['ename'])
    name.append(body[i]['cname'])

zhonglan = []
shu = range(len(h))
huizong = []
for j in shu:
    url3 = 'https://pvp.qq.com/web201605/herodetail/' + str(h[j]) + '.shtml'
    rs02 = requests.get(url3, headers=ua)
    rs02.encoding = "gbk"
    body02 = rs02.text
    html02 = etree.HTML(body02)
    shuju = html02.xpath('//i[contains(@style,"width")]/@style')
    for k in range(len(shuju)):
        shuju[k] = int(shuju[k][6:-2])
    shuju.insert(0, name[j])
    huizong.append(shuju)

print(len(huizong))

# 数据处理
df = pd.DataFrame(huizong, columns=["英雄名字", "生存能力", "攻击伤害", "技能效果", "上手难度"])
# 根据生存能力的排序操作,从大到小排序
df = df.sort_values(by="攻击伤害", ascending=False)
pd.set_option('display.max_rows', None)  # 显示所有行
print(len(df))
# 把数据转换成列表,取出英雄名字
x = list(df["英雄名字"])[0:10]
print(x)
y = list(df["攻击伤害"])[0:10]
print(y)

# 画图
b = Bar()
b.add_xaxis(x)
b.add_yaxis("王者荣耀英雄攻击伤害前10排名", y)
# 翻转
b.reversal_axis()
b.render("../../A2兼收并蓄/王者荣耀英雄攻击伤害前10排名.html")
