# coding=utf-8
# @Time    : 2024/11/25 17:52
# @Software: PyCharm
import os
import re

"""
单纯的将 '第xx章' 替换为 '# 第xx章'
"""

# 构建文件路径(桌面上的文件)
input_file_path = os.path.join(os.path.expanduser("~"), "Desktop/十日终焉.txt")
output_file_path = os.path.join(os.path.expanduser("~"), "Desktop/十日终焉.md")
results = [r"""---
title: 《十日终焉》
language: zh-CN
---
"""]

# 正式处理
pattern1 = re.compile(r'第\d+章')
pattern2 = re.compile(r'第[一二三四五六七八九十百]+卷：')
# 读取文件
with open(input_file_path, "r", encoding='utf-8') as f:
    for line in f:
        # '第xx章'、'第xx卷' 前面加上 '# '
        if line.startswith('第'):
            if pattern1.match(line) or pattern2.match(line):
                line = '# ' + line
        # 正文缩进替换为4个空格(在起点、番茄等于1个汉字长度)
        elif line.startswith('    '):
            line = line.replace("    ", "&nbsp;" * 4)
        # 分割下划线前加入换行符
        elif line.startswith('------------'):
            line = "\n" + line
        results.append(line)

# 将替换后的内容写回文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    for line in results:
        file.write(line)
