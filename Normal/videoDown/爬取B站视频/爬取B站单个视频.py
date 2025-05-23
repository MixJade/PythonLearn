# 爬取B站的视频 Bilibili
# B站的视频地址是直接存储在源网页中的，因此只需要从源网页中解析即可

import json
import os
import re

import requests
from lxml import html

"""遇到下载不了的，可以在手机上缓存
手机存储路径：Android/data/tv.danmaku.bili/download
然后上传到电脑上，执行：

ffmpeg -i video.m4s -i audio.m4s -acodec copy -vcodec copy testout.mp4
"""

# 选择一个视频的url(如果是分p视频则放上完整url)
url = r'https://www.bilibili.com/video/BV1494y147mF'

# 保存路径(斜线结尾)
dir_path = r"../../outputFile/creepB2/"

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# 设置请求头(想下载更高的清晰度需先登录，再加上Cookie)
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 "
                  "Safari/537.36 Edg/118.0.2088.76",
    "Referer": "https://www.bilibili.com/",  # 设置防盗链
}

resp = requests.get(url=url, headers=header)


def get_video_title(html_content: str) -> str:
    """获取视频标题
    """
    tree = html.fromstring(html_content)
    xpath_expr = '//h1[contains(@class, "video-title") and contains(@class, "special-text-indent")]'
    elements = tree.xpath(xpath_expr)
    if elements:
        # 获取第一个匹配元素的文本内容
        return elements[0].text_content().strip()
    else:
        return "未获得视频名"


video_name = get_video_title(resp.text)
print("视频名称：" + video_name)

obj = re.compile(r'window.__playinfo__=(.*?)</script>', re.S)
html_data = obj.findall(resp.text)[0]  # 从列表转换为字符串
# 转化为字典的形式
json_data = json.loads(html_data)

# video 和 audio分别是视频和音频 因此爬取下来以后，还需要将两个合并
videos = json_data['data']['dash']['video']  # 这里得到的是一个列表
# 只需要baseUrl即可
print(videos[0])  # 只有视频有清晰度区分，如果id不是80说明没加cookie
video_url = videos[0]['baseUrl']  # 视频地址

# 同理，音频地址为
audios = json_data['data']['dash']['audio']
audio_url = audios[0]['baseUrl']

resp1 = requests.get(url=video_url, headers=header)

print("视频地址:" + video_url)
with open(dir_path + 'test_ori.mp4', mode='wb') as f:
    f.write(resp1.content)

resp2 = requests.get(url=audio_url, headers=header)

print("音频地址:" + audio_url)
with open(dir_path + f'test_ori.mp3', mode='wb') as f:
    f.write(resp2.content)

print("爬取完成")

# 现在需要将视频和音频合并 需要模块ffmpeg
command = f'ffmpeg -i test_ori.mp4 -i test_ori.mp3 -acodec copy -vcodec copy {video_name}.mp4'
os.chdir(dir_path)  # 切换到目标目录
os.system(command=command)

print(f"文件已保存至：{dir_path}{video_name}.mp4")
