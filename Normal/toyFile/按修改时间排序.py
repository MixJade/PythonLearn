# coding=utf-8
# @Time    : 2024/9/17 11:15
# @Software: PyCharm
import os
from datetime import datetime

# 指定要查看的目录
directory = "文本处理"

# 获取目录下所有文件，不包括子目录
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# 获取每个文件的修改时间并放入一个字典中
files_modification_time = {f: os.path.getmtime(os.path.join(directory, f)) for f in files}

# 按照修改时间排序文件名
files_sorted_by_time = sorted(files_modification_time.items(), key=lambda item: item[1])

# 打印文件名和修改时间
for f, timestamp in files_sorted_by_time:
    # 将时间戳转换为可读的格式
    mod_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print(f"文件: {f: <20}修改时间: {mod_time}")
