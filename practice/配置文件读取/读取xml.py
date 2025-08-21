# coding=utf-8
# @Time    : 2025/8/21 10:18
# @Software: PyCharm
from lxml import etree

# 读取并解析XML
with open("testRead/测试读取.xml", 'rb') as xml_file:
    xml_tree = etree.parse(xml_file)

# 提取数据示例
root = xml_tree.getroot()

# 遍历所有字典
for dict1 in root.xpath('//dict'):
    dic_code = dict1.get('code')
    dic_name = dict1.get('name')
    # 可选属性,但读取的都是字符串，必须转换
    begin_seq = int(dict1.get('beginSeq', '0'))

    print(f"\n字典编码: {dic_code}")
    print(f"字典名称: {dic_name}")
    print(f"起始序列: {begin_seq}")
    print("参数列表:")

    # 遍历当前字典的参数
    for parm in dict1.xpath('./parm'):
        print(f"  code: {parm.get('code')}, name: {parm.get('name')}")
