# coding=utf-8
# @Time    : 2024/11/25 17:52
# @Software: PyCharm
import os
import re

"""处理小说《蛊真人》
"""

# 构建文件路径(桌面上的文件)
input_file_path = r"C:\MyCode\selfTool\chat\chatFile\39007.txt"

results = []

# 正式处理
pattern1 = re.compile(r'第[零一二两三四五六七八九十百]+节：')
pattern2 = re.compile(r'第[零一二两三四五六七八九十百]+卷：')
# 读取文件
with open(input_file_path, "r", encoding='utf-8') as f:
    for line in f:
        if line.startswith('第'):
            # '第xx节'前面加上 '# '
            if pattern1.match(line):
                line = '# ' + line
            # “第xx卷”则去掉
            elif pattern2.match(line):
                line = '\n'
        # 分割下划线前加入换行符
        elif line.startswith('------------'):
            line = "\n" + line
        # 正文缩进替换为4个特殊空格
        elif line != "\n":
            line = "　　" + line.strip(" ")
        results.append(line)

output_dir = os.path.join(os.path.expanduser("~"), "Desktop")
md_name = f"蛊真人"
output_file_path = os.path.join(output_dir, md_name + ".md")
# 将替换后的内容写回文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(f"---\ntitle: 《{md_name}》\nlanguage: zh-CN\n---\n\n")
    for line in results:
        file.write(line)
