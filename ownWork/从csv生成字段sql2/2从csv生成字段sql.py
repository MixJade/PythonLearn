# coding=utf-8
# @Time    : 2025/7/21 15:01
# @Software: PyCharm
import pandas as pd

from utils.convertCase import camel_to_snake
from utils.outFieldSQL import SqlParam, out_db_sql

# 读取两个csv文件
data1 = pd.read_csv(r'新增的字段_结果.csv')

# 需新增字段的表
table_name = "STUDENT_INF"
table_comment = "学生表"

# 保证列相同
data1 = data1[['NAME', 'COMMENT', 'LENGTH']]

# 输出字段
sql_param_list: list[SqlParam] = []

for index, row in data1.iterrows():
    sql_param_list.append(SqlParam(
        java_name=row["NAME"],
        comment=row["COMMENT"],
        sql_field=camel_to_snake(row["NAME"]),
        type_len=row["LENGTH"]
    ))

out_db_sql(sql_param_list, table_name, table_comment)
