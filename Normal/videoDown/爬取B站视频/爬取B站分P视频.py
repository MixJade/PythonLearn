# coding=utf-8
# @Time    : 2025-04-03 21:51
# @Software: PyCharm

import json
import os
import re

import requests

"""下载某分P的所有视频
"""
# 选择一个视频的url(如果是分p视频则带上最后的p参数，但不要放“p=”后的那个数字)
url = r'https://www.bilibili.com/video/BV1YLoYYcEyx/?spm_id_from=3333&p='
# 开始和结束分P
begin_p, en_p = 2, 32

# 保存路径(斜线结尾)
dir_path = r"../../outputFile/creepB2P/"

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# 设置请求头(想下载更高的清晰度需先登录，再加上Cookie)
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 "
                  "Safari/537.36 Edg/118.0.2088.76",
    "Referer": "https://www.bilibili.com/",  # 设置防盗链
}
en_p = en_p + 1
for i in range(begin_p, en_p):
    print(f"========================[下载第{i}P]================================")
    resp = requests.get(url=f"{url}{i}", headers=header)
    # 这个baseUrl就是视频的地址
    obj = re.compile(r'window.__playinfo__=(.*?)</script>', re.S)
    html_data = obj.findall(resp.text)[0]  # 从列表转换为字符串
    # 转化为字典的形式
    json_data = json.loads(html_data)
    # 格式化输出
    # video 和 audio分别是视频和音频 因此爬取下来以后，还需要将两个合并
    videos = json_data['data']['dash']['video']  # 这里得到的是一个列表
    # 只需要baseUrl即可
    video_url = videos[0]['baseUrl']  # 视频地址
    # 同理，音频地址为
    audios = json_data['data']['dash']['audio']
    audio_url = audios[0]['baseUrl']
    resp1 = requests.get(url=video_url, headers=header)
    print("视频地址:" + video_url)
    with open(f'{dir_path}test{i}.mp4', mode='wb') as f:
        f.write(resp1.content)
    resp2 = requests.get(url=audio_url, headers=header)
    print("音频地址:" + audio_url)
    with open(f'{dir_path}test{i}.mp3', mode='wb') as f:
        f.write(resp2.content)

print("=============================[爬取完成]=======================================")
# 现在需要将视频和音频合并 需要模块ffmpeg
os.chdir(dir_path)  # 切换到目标目录
for i in range(begin_p, en_p):
    command = f'ffmpeg -i test{i}.mp4 -i test{i}.mp3 -acodec copy -vcodec copy testout{i}.mp4'
    os.system(command=command)
