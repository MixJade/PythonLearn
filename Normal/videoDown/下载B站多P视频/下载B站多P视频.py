# coding=utf-8
# @Time    : 2025/2/22 9:58
# @Software: PyCharm
import os

"""使用you-get进行下载
pip install you-get
"""

# 要下载的视频bv号
bv = "BV1YLoYYcEyx"
# 其它配置，注意先去处理cookie，不然480p
download_path = "../../outputFile/videos"

try:
    command = f"you-get --playlist -o {download_path} https://www.bilibili.com/video/{bv}"
    os.system(command)
    print("视频下载完成！")
except Exception as e:
    print(f"下载过程中出现错误：{e}")
