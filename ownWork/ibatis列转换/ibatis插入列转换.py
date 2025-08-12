# coding=utf-8
# @Time    : 2025/8/11 18:23
# @Software: PyCharm
from utils.convertCase import snake_to_camel
from utils.ibatisOut import IBatisParam, out_update_col, out_result_map

param_list: list[IBatisParam] = []
with open('tesIBatis/ibatis插入列.txt', 'r') as file:
    for line in file:
        if line.endswith(",\n"):
            line = line[:-2]
        param_list.append(IBatisParam(sql_column=line, java_field=snake_to_camel(line)))

# 查询列变更新列
out_update_col(param_list)
# 查询列变结果集
out_result_map(param_list)
