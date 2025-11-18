# coding=utf-8
# @Time    : 2025/10/31 16:42
# @Software: PyCharm
import os
from lxml import etree
from typing import NamedTuple

"""
批量替换多个文件中的字符串
"""

# 读取并解析XML
with open("变更内容配置.xml", 'rb') as xml_file:
    xml_tree = etree.parse(xml_file)
root = xml_tree.getroot()


class ChangeParam(NamedTuple):
    old_str: str  # 旧字符串
    new_str: str  # 新字符串


# 文件列表
file_list: list[str] = []
for file1 in root.xpath('//fileList'):
    for index, parm in enumerate(file1.xpath('./file')):
        file_list.append(parm.get('path'))

# 变更列表
change_list: list[ChangeParam] = []
for change1 in root.xpath('//changeList'):
    for index, parm in enumerate(change1.xpath('./change')):
        old_str = parm.get('old')
        new_str = parm.get('new')
        change_list.append(ChangeParam(old_str, new_str))

# 开始替换
for file_path in file_list:
    print(f"\n开始替换文件: {file_path}")
    if not os.path.isfile(file_path):
        print(f"错误: 文件 '{file_path}' 不存在")
        continue
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # 替换字符串
        for change in change_list:
            if change.old_str in content:
                content = content.replace(change.old_str, change.new_str)
                print(" " * 4 + f"{change.old_str} --> {change.new_str}")
            else:
                print(" " * 4 + f"No find: {change.old_str}")
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print("替换完成")
    except Exception as e:
        print(f"处理文件 '{file_path}' 时出错: {e}")
