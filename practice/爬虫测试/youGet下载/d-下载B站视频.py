# coding=utf-8
# @Time    : 2025/2/22 9:58
# @Software: PyCharm
import os

"""使用you-get进行下载
pip install you-get
"""

# 要下载的视频bv号
bv = "BV1ccUBYqEUc"
# 其它配置，注意先去处理cookie，不然480p
download_path = "../../outputFile/videos"
cookie_file_path = r"b-cookies.txt"

try:
    # 实际命令，后面的debug可以去掉
    command = f"you-get --c {cookie_file_path} -o {download_path} https://www.bilibili.com/video/{bv} --debug"
    os.system(command)
    print("视频下载完成！")
except Exception as e:
    print(f"下载过程中出现错误：{e}")
