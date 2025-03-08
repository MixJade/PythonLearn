# coding=utf-8
# @Time    : 2024/2/14 17:51
# @Software: PyCharm
import re

"""处理包括：去除括号包裹内容、消除空格、句子末尾添加换行、紧凑的两行插入空行
"""
file_name = r"../文本处理/data/测试章节拆分.txt"

# 使用 'r' 模式打开文件进行读取
with open(file_name, 'r', encoding='utf8') as f:
    content = f.read()
    # 移除括号包裹内容,如“不见（xian）可欲”只留下“不见可欲”
    content = re.sub(r'（.*?）', '', content)
    content = re.sub(r'\(.*?\)', '', content)

# 一、去除文件中的所有空格
# 使用 replace() 函数替换所有的空格
new_content = content.replace(" ", "")
# 去掉商标
new_content = new_content.replace("上一", "")

# 二、在句子的末尾加上换行
new_content = new_content.replace("。", "。\n")
new_content = new_content.replace("。\n”", "。”\n")  # 防止引用内容被错误换行
new_content = new_content.replace("？", "。\n")
new_content = new_content.replace("！", "。\n")

# 使用 'w' 模式打开文件进行写入
with open(file_name, 'w', encoding='utf8') as f:
    f.write(new_content)

"""
当有两行文字挨在一起时，在其中插入空行，没有挨着则不插入
"""
# 打开原始文件
with open(file_name, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 对文字进行处理并写入新文件
with open(file_name, 'w', encoding='utf-8') as f:
    # 用一个标志位记录上一行是否为空行
    last_line_was_blank = True
    for line in lines:
        # 如果当前行不为空且上一行也不为空，那么在当前行前插入一个空行
        if line.strip() != '' and not last_line_was_blank:
            f.write("\n")
        f.write(line)
        # 更新标志位
        last_line_was_blank = line.strip() == ''
