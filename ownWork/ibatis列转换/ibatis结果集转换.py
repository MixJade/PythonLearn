# coding=utf-8
# @Time    : 2025/8/8 14:43
# @Software: PyCharm
from lxml import etree
from utils.convertCase import snake_to_camel
from utils.ibatisOut import *

parser = etree.XMLParser(remove_blank_text=True)  # 保留空白格式
tree = etree.parse('tesIBatis/ibatis结果集.xml', parser)
root = tree.getroot()

# 查找所有 result 和 id 标签
result_elements = root.xpath('.//result | .//id')

param_list: list[IBatisParam] = []

# 提取 column 属性
for idx, element in enumerate(result_elements):
    column_name = element.get('column')
    table_str = column_name
    param_list.append(IBatisParam(
        sql_column=column_name,
        java_field=snake_to_camel(column_name)
    ))

# CDATA格式的插入列
out_insert_cdata_col(param_list)
# CDATA格式的更新列
out_update_cdata_col(param_list)
# 正常的查询列
out_select_col(param_list)
# 正常的插入列
out_insert_col(param_list)
# 正常的更新列
out_update_col(param_list)
