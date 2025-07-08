# coding=utf-8
# @Time    : 2025/7/8 16:12
# @Software: PyCharm
from lxml import etree

parser = etree.XMLParser(remove_blank_text=True)  # 保留空白格式
tree = etree.parse('ibatis的结果集.xml', parser)
root = tree.getroot()

# 查找所有 result 和 id 标签
result_elements = root.xpath('.//result | .//id')

column_list = []
# 提取 column 属性
for element in result_elements:
    column_list.append(element.get('column'))

# 使用 join() 方法将列表元素用逗号连接成字符串
result_str = ",".join(column_list)
# 打印结果
print("查询结果列：\n")
print(result_str)
