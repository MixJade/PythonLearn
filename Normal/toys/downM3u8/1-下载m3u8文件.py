# coding=utf-8
# @Time    : 2024/8/23 22:49
# @Software: PyCharm
import os
import time

import requests

headers = {'User-Agent': 'Mozilla/5.0'}

# 输出文件夹路径
out_put_dir = "../../outputFile/downM3u8/"
# 新建一个文件夹用于存放.ts文件
if not os.path.exists(out_put_dir):
    os.makedirs(out_put_dir)

# m3u8网址
base_url = 'https://example.com/path/'
m3u8_name = 'index.m3u8'
# 继续下载文件名,第一次是空的，但后面的就类似于：xxx.ts
keep_on_file_name = ""
now_keep_on = (keep_on_file_name != "")  # 跳过第一次
# 下载m3u8
if not now_keep_on:
    print(f"下载{m3u8_name}")
    response = requests.get(base_url + m3u8_name, headers=headers)
    with open(out_put_dir + m3u8_name, 'wb') as f:
        f.write(response.content)


# 下载key(如果m3u8有加密的话)
# if not now_keep_on:
#     key_name = 'key.dat'
#     print(f"下载{key_name}")
#     response2 = requests.get(base_url + key_name, headers=headers)
#     with open(out_put_dir + key_name, 'wb') as f:
#         f.write(response2.content)


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


# 2024-09-15 04:25:14 加入即使出现异常也会继续下载的功能
result_list = read_m3u8_to_ts(out_put_dir + m3u8_name)
# 正式逻辑
while True:
    # noinspection PyBroadException
    try:
        for index, ts_name in enumerate(result_list, start=1):
            if now_keep_on:
                if ts_name != keep_on_file_name:
                    continue
                else:
                    now_keep_on = False
            print(f"({index}/{len(result_list)})下载{ts_name}")
            keep_on_file_name = ts_name  # 做备份
            # 下载
            response = requests.get(base_url + ts_name,
                                    headers=headers)
            with open(out_put_dir + ts_name, 'wb') as f:
                f.write(response.content)
    # 假设只有请求超时异常,但防止其它情况，需捕获所有异常
    except Exception as e:
        # 一般都是这个异常：requests.exceptions.ConnectTimeout
        print(f"出现异常{type(e)},等待15秒后继续执行，当前文件:{keep_on_file_name}")
        print("异常实例：", e)
        # 异常重试机制
        time.sleep(15)
        now_keep_on = True
        continue
    else:
        print("结束了")
        break
