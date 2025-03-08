# coding=utf-8
# @Time    : 2024/11/25 17:52
# @Software: PyCharm
import os
import re

# noinspection HttpUrlsUsage
"""处理小说《十日终焉》

下载地址：http://www.mayitxt.org/down/txt180753.html
"""

# 构建文件路径(桌面上的文件)
input_file_path = os.path.join(os.path.expanduser("~"), "Desktop/十日终焉.txt")

"""一、正文处理
"""
results = []

# 正式处理
pattern1 = re.compile(r'第\d+章')
pattern2 = re.compile(r'第[一二三四五六七八九十百]+卷：')
pattern3 = re.compile(r'# 第[一二三四五六七八九十百]+卷：')
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

"""二、拆分分卷
"""
# 初始化临时列表和结果列表
temp = []
res = []

# 遍历原始列表
for i in results:
    # 如果元素符合 '# 第xx卷' 格式
    if i.startswith("# 第") and pattern3.match(i):
        # 如果临时列表不为空，将临时列表添加到结果列表
        if temp:
            res.append(temp)
            temp = []
    # 将元素添加到临时列表
    temp.append(i)

# 将最后的临时列表添加到结果列表
if temp:
    res.append(temp)

print(f"共{len(res)}卷")

# 检查对应文件夹是否存在
output_dir = os.path.join(os.path.expanduser("~"), f"Desktop/十日终焉")
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

for index, item in enumerate(res):
    md_name = f"十日终焉{index:02d}.md"
    output_file_path = os.path.join(output_dir, md_name)
    # 将替换后的内容写回文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(f"---\ntitle: 《{md_name}》\nlanguage: zh-CN\n---\n\n")
        for line in item:
            file.write(line)
