# coding=utf-8
# @Time    : 2025/8/4 16:03
# @Software: PyCharm
from lxml import etree
from utils.convertCase import snake_to_camel

parser = etree.XMLParser(remove_blank_text=True)  # 保留空白格式
tree = etree.parse('ibatis的结果集.xml', parser)
root = tree.getroot()

# 查找所有 result 和 id 标签
result_elements = root.xpath('.//result | .//id')

# 提取 column 属性
for element in result_elements:
    column_name = element.get('column')
    print(f'<isNotEmpty property="{snake_to_camel(column_name)}" prepend=",">{column_name}=#{snake_to_camel(column_name)}#</isNotEmpty>')
