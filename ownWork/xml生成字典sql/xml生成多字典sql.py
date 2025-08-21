# coding=utf-8
# @Time    : 2025/8/6 17:44
# @Software: PyCharm
from lxml import etree

from utils.outDictSQL import *

# 解析 XML 文件（使用lxml的解析器）
# 读取并解析XML
with open("多字典及其码值.xml", 'rb') as xml_file:
    xml_tree = etree.parse(xml_file)
root = xml_tree.getroot()

# 遍历每个分组并填入
dic_list: list[DicMain] = []
# 遍历所有字典
for dict1 in root.xpath('//dict'):
    dic_code = dict1.get('code')
    dic_name = dict1.get('name')
    begin_seq = int(dict1.get('beginSeq', '0'))  # 字典起始排序,默认为0
    # 当起始序列为0时,是整个字典新增,否则默认是追加
    is_new = (begin_seq == 0)
    # 读取字典下的参数列表
    dic_param_list: list[DicParam] = []
    for index, parm in enumerate(dict1.xpath('./parm')):
        dic_param_list.append(DicParam(seq=index + begin_seq, code=parm.get('code'), name=parm.get('code')))
    dic_list.append(DicMain(code=dic_code, name=dic_name, is_new=is_new, parm_list=dic_param_list))

# 探查
print("\n-- " + "=" * 50)
for dic in dic_list:
    out_hy_dic_sql(dic, is_hy=False)
# 插入数据
print("\n-- " + "=" * 50)
for dic in dic_list:
    out_insert_dic_sql(dic)
# 核验
print("\n-- " + "=" * 50)
for dic in dic_list:
    out_hy_dic_sql(dic)
