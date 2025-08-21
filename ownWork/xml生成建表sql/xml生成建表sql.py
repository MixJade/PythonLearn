# coding=utf-8
# @Time    : 2025/8/6 14:32
# @Software: PyCharm
from lxml import etree

from utils.convertCase import camel_to_snake
from utils.outFieldSQL import *

with open(r"字段及注释_小驼峰.xml", 'rb') as xml_file:
    xml_tree = etree.parse(xml_file)
root = xml_tree.getroot()

# 遍历每个分组并填入
sql_param_list: list[SqlParam] = []
# 遍历所有表配置
for table in root.xpath('//table'):
    # 遍历当前表字段
    for field in table.xpath('./field'):
        sql_param_list.append(SqlParam(
            java_name=field.get('code'),
            comment=field.get('name'),
            sql_field=camel_to_snake(field.get('code')),
            type_len=field.get('length')
        ))
    # 生成建表SQL
    out_create_table_sql(sql_param_list, table.get('code'), table.get('name'))
    # 解开以下语句就是追加字段SQL
    # out_db_sql(sql_param_list, table.get('code'), table.get('name'))
