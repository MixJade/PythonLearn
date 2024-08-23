# coding=utf-8
# @Time    : 2024/8/23 22:49
# @Software: PyCharm
import os

import requests

headers = {'User-Agent': 'Mozilla/5.0'}

# 输出文件夹路径
out_put_dir = "../../outputFile/downM3u8/"
# 新建一个文件夹用于存放.ts文件
if not os.path.exists(out_put_dir):
    os.mkdir(out_put_dir)

# m3u8网址
base_url = 'https://example.com/path/'
m3u8_name = 'index.m3u8'
key_name = 'key.dat'
# 下载m3u8
response = requests.get(base_url + m3u8_name, headers=headers)
with open(out_put_dir + m3u8_name, 'wb') as f:
    f.write(response.content)

# 下载key(如果m3u8有加密的话)
response2 = requests.get(base_url + key_name, headers=headers)
with open(out_put_dir + key_name, 'wb') as f:
    f.write(response2.content)


# 解析m3u8并下载TS文件
def read_m3u8_to_ts(file_path: str) -> list[str]:
    """解析m3u8的ts名称"""
    # 读取文件所有的行
    with open(file_path, 'r') as ts_f:
        lines = ts_f.readlines()
    # 存储'#EXTINF'开头行的下一行
    result = []
    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF'):
            # 由于列表索引从0开始，所以下一行是lines[i+1]
            result.append(lines[i + 1].strip())  # 使用strip()移除末尾的换行符
    return result


for ts_name in read_m3u8_to_ts(out_put_dir + m3u8_name):
    print(f"下载{ts_name}")
    response = requests.get(base_url + ts_name,
                            headers=headers)
    with open(out_put_dir + ts_name, 'wb') as f:
        f.write(response.content)
