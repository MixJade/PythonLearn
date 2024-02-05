import requests
import xlwt
from lxml import etree

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
print(huizong[1][3])

workbook = xlwt.Workbook(encoding='utf-8')  # 设置一个workbook，其编码是utf-8
worksheet = workbook.add_sheet("herodata")  # 新增一个sheet
worksheet.write(0, 0, label='英雄ID')
worksheet.write(0, 1, label='英雄名字')  # 将‘列1’作为标题
worksheet.write(0, 2, label='生存能力')
worksheet.write(0, 3, label='攻击伤害')  # 将‘列1’作为标题
worksheet.write(0, 4, label='技能效果')
worksheet.write(0, 5, label='上手难度')  # 将‘列1’作为标题

for i in range(len(huizong)):  # 循环将a和b列表的数据插入至excel
    worksheet.write(i + 1, 0, label=i)
    for j in range(5):
        worksheet.write(i + 1, j + 1, label=huizong[i][j])
workbook.save("../../A2兼收并蓄/王者英雄数据.xls")  # 这里save需要特别注意，文件格式只能是xls
