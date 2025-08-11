# coding=utf-8
# @Time    : 2025/8/11 18:23
# @Software: PyCharm
from utils.convertCase import snake_to_camel
from typing import NamedTuple


class IBatisParam(NamedTuple):
    sql_column: str  # SQL字段名称,形如:PRJ_NAME
    java_field: str  # 实体类中字段名称,形如:prjName


param_list: list[IBatisParam] = []
with open('ibatis的插入列.txt', 'r') as file:
    for line in file:
        if line.endswith(",\n"):
            line = line[:-2]
        param_list.append(IBatisParam(sql_column=line, java_field=snake_to_camel(line)))

for index, param in enumerate(param_list):
    res_str = f'{param.sql_column}=#{param.java_field}#'
    if index != len(param_list) - 1:
        res_str += ","
    # 解开下面的注释：查询列变结果集
    # res_str = f'<result property="{param.java_field}" column="{param.sql_column}"/>'
    print(res_str)
