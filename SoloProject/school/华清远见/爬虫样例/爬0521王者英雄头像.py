import requests

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

print(len(h))

url2 = 'https://game.gtimg.cn/images/yxzj/img201606/heroimg/'
for j in range(len(h)):
    listurl2 = url2 + str(h[j]) + '/' + str(h[j]) + '.jpg'
    print(listurl2)
    rs2 = requests.get(listurl2, headers=ua)
    img = rs2.content
    path = "../../A2兼收并蓄/%s.jpg" % (name[j])
    with open(path, 'wb') as f:
        f.write(img)
