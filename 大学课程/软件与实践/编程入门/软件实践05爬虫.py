# coding=utf-8
# @Time    : 2021/11/23 16:30
# @Software: PyCharm
import requests
from lxml import etree

"""使用爬虫抓取下载自己喜欢的网易云音乐歌单
"""

url = "https://music.163.com/playlist?id=6686195225"
base_url = 'https://link.hhtjim.com/163/'  # 外链地址
# noinspection SpellCheckingInspection
ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
AppleWebKit/537.36 (KHTML, like Gecko) \\Chrome/86.0.4240.198 Safari/537.36"'}
# 2. 请求 content：
html_str = requests.get(url, headers=ua).text
html_dom = etree.HTML(html_str)  # 将字符串转化为真正的 html
# 3. 删选数据 xpath
song_names = html_dom.xpath('//a[contains(@href,"song?id=")]/text()')
song_ids = html_dom.xpath('//a[contains(@href,"song?id=")]/@href')

for song_name, song_id in zip(song_names, song_ids):
    if '{' in song_name:  # 去除名字中出现 { 的情况
        continue
    print(song_name)
    count_id = song_id.strip('/song?id=')

    if not ('$' in count_id):
        print(count_id)
        song_url = base_url + count_id + '.mp3'
        print(song_url)

        m4a = requests.get(song_url).content
        # 4. 保存数据
        with open('../../A2兼收并蓄/%s.mp3' % song_name, "wb") as file:
            file.write(m4a)
