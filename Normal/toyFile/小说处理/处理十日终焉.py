# coding=utf-8
# @Time    : 2024/11/25 17:52
# @Software: PyCharm
import os
import re

"""
单纯的将 '第xx章' 替换为 '# 第xx章'
"""

# 构建文件路径(桌面上的文件)
file_path = os.path.join(os.path.expanduser("~"), "Desktop/十日终焉.txt")
results = []
pattern1 = re.compile(r'第\d+章')
# 读取文件
with open(file_path, "r", encoding='utf-8') as f:
    for line in f:
        if line.startswith('第'):
            # 判断该章节标题是否已经被标号
            if pattern1.match(line):
                line = '# ' + line
        results.append(line)

# 将替换后的内容写回文件
with open("output_file.mds", 'w', encoding='utf-8') as file:
    for line in results:
        file.write(line)
