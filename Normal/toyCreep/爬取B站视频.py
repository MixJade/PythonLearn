# 爬取B站的视频 Bilibili
# B站的视频地址是直接存储在源网页中的，因此只需要从源网页中解析即可

import json
import os
import re

import requests

# 选择一个视频 ，只需要前半部分就可以啦
url = r'https://www.bilibili.com/video/BV1Ck4y197i1/'

# 保存路径(斜线结尾)
dir_path = r"../outputFile/creepB2/"

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# 设置请求头(想下载更高的清晰度需先登录，再加上Cookie)
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 "
                  "Safari/537.36 Edg/118.0.2088.76",
    "Referer": "https://www.bilibili.com/",  # 设置防盗链
}

resp = requests.get(url=url, headers=header)
# print(resp.text) #成功获取

# 这个baseUrl就是视频的地址

obj = re.compile(r'window.__playinfo__=(.*?)</script>', re.S)
html_data = obj.findall(resp.text)[0]  # 从列表转换为字符串
# print(html_data)
# 转化为字典的形式
json_data = json.loads(html_data)
# 格式化输出
# pprint(json_data)
# video 和 audio分别是视频和音频 因此爬取下来以后，还需要将两个合并

videos = json_data['data']['dash']['video']  # 这里得到的是一个列表
# 只需要baseUrl即可
print(videos)
video_url = videos[0]['baseUrl']  # 视频地址

# 同理，音频地址为

audios = json_data['data']['dash']['audio']
audio_url = audios[0]['baseUrl']

resp1 = requests.get(url=video_url, headers=header)

print("视频地址:" + video_url)
