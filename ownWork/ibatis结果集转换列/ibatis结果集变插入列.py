# coding=utf-8
# @Time    : 2025/8/8 14:43
# @Software: PyCharm
from lxml import etree
from utils.convertCase import snake_to_camel

parser = etree.XMLParser(remove_blank_text=True)  # 保留空白格式
tree = etree.parse('ibatis的结果集.xml', parser)
root = tree.getroot()

# 查找所有 result 和 id 标签
result_elements = root.xpath('.//result | .//id')

tableField: list[str] = []  # 表的字段列表
javaField: list[str] = []  # 代码的字段列表
# 提取 column 属性
for idx, element in enumerate(result_elements):
    column_name = element.get('column')
    table_str = column_name
    java_str = f"#{snake_to_camel(column_name)}#"
    if not idx == len(result_elements) - 1:  # 不是最后一个元素则逗号结尾
        table_str += ','
        java_str += ','
    tableField.append(table_str)
    javaField.append(java_str)

# noinspection SqlNoDataSourceInspection
print("<![CDATA[\nINSERT INTO XXX(")
for val in tableField:
    print(f"\t{val}")
print(f") VALUES (")
for jf in javaField:
    print(f"\t{jf}")
print(")\n]]>")
