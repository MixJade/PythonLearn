# coding=utf-8
# @Time    : 2024-12-05 09:57:58
# @Software: PyCharm
import os

"""给md小说，每段的前面加四个空格
"""

# 构建文件路径(桌面上的文件)
input_file_path = os.path.join(os.path.expanduser("~"), "Desktop/娱乐至死.md")
output_file_path = os.path.join(os.path.expanduser("~"), "Desktop/娱乐至死(空格版).md")
"""一、正文处理
"""
results = []

# 读取文件
with open(input_file_path, "r", encoding='utf-8') as f:
    for line in f:
        if not (line.startswith('---')
                or line.startswith('#')
                or line == '\n'
                or line.startswith('title')
                or line.startswith('language')):
            line = "&nbsp;" * 4 + line
        results.append(line)

"""二、输出文件
"""
# 将替换后的内容写回文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    for line in results:
        file.write(line)
