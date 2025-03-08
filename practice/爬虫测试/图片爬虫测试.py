import requests
from lxml import etree

# 爬去网页图片，并下载到本地
url = "http://pic.netbian.com/"
# 向目标网站发送请求并获取网页源码
rs = requests.get(url)
# 指定字符集
rs.encoding = "gbk"
# 网页源码
body = rs.text
# print(body)
html = etree.HTML(body)
listImg = html.xpath("//ul[@class='clearfix']/li/a/span/img/@src")
print("图片：", listImg)

for i in range(len(listImg)):
    # 拼接图片路径
    file_path = url + listImg[i]
    # 获取response对象
    rs = requests.get(file_path)
    # 获取图片的二进制文本
    img = rs.content
    # 保存路径
    path = f"../outputFile/图片{i}.gif"
    with open(path, 'wb') as f:
        f.write(img)
