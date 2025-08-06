# coding=utf-8
# @Time    : 2025/8/6 14:32
# @Software: PyCharm
import pandas as pd
from utils.outFieldSQL import SqlParam, out_create_table_sql
from utils.convertCase import camel_to_snake

data1 = pd.read_csv('字段及对应注释.csv')
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

# 把这里换一下就是生成字段了
out_create_table_sql(sql_param_list, table_name, table_comment)
