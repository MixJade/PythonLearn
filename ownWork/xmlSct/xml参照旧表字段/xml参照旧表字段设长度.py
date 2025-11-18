# coding=utf-8
# @Time    : 2025/8/26 17:20
# @Software: PyCharm
from lxml import etree

"""读取旧表的字段
"""
with open(r"多张旧表结构.xml", 'rb') as xml_file:
    xml_tree = etree.parse(xml_file)
old_root = xml_tree.getroot()

# 旧表的字段map
old_field_map = {}

# 遍历所有表配置
for table in old_root.xpath('//table'):
    # 遍历当前表字段\长度，如有重复，以最后的为准
    for field in table.xpath('./field'):
        old_field_map[field.get('code')] = field.get('length')

"""开始处理新版的字段
"""
input_xml = r"待新增的字段.xml"
with open(input_xml, 'rb') as xml_file:
    xml_tree = etree.parse(xml_file)
root = xml_tree.getroot()
for table in root.xpath('//table'):
    # 遍历当前表字段
    for field in table.xpath('./field'):
        # 没有匹配上
        field.set('length', old_field_map.get(field.get('code'), ""))

"""写回XML文件
"""
xml_tree.write(input_xml,
               encoding='UTF-8',
               xml_declaration=True,
               pretty_print=True)  # 添加漂亮打印格式

print(f"排序和重新编号完成，结果已保存到 {input_xml}")
