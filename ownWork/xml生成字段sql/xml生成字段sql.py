# coding=utf-8
# @Time    : 2025/8/21 10:59
# @Software: PyCharm
from lxml import etree
from utils.outFieldSQL import SqlParam, out_db_sql
from utils.convertCase import small_snake_to_camel

with open(r"字段及注释_小蛇形.xml", 'rb') as xml_file:
    xml_tree = etree.parse(xml_file)
root = xml_tree.getroot()

# 遍历每个分组并填入
sql_param_list: list[SqlParam] = []
# 遍历所有表配置
for table in root.xpath('//table'):
    # 遍历当前表字段
    for field in table.xpath('./field'):
        sql_param_list.append(SqlParam(
            java_name=small_snake_to_camel(field.get('code')),
            comment=field.get('name'),
            sql_field=field.get('code').upper(),
            type_len=field.get('length')
        ))
    out_db_sql(sql_param_list, table.get('code'), table.get('name'))
