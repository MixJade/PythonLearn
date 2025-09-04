# coding=utf-8
# @Time    : 2025/9/4 17:45
# @Software: PyCharm
import pandas as pd

# 读取CSV文件(如果读取失败，请将对应csv文件转为utf8格式)
df2 = pd.read_csv('系列对应名称.csv')
df2 = df2[['系列编号', '系列名称', '项目简称命名规则']]

# 分组输出
groups = df2.groupby('项目简称命名规则')
grouped_list = [group for _, group in groups]

for group in grouped_list:
    group_name = ""
    content_1 = []
    content_2 = []
    for index, row in group.iterrows():
        group_name = row["项目简称命名规则"]
        content_1.append(f"'{row['系列编号']}'")
        content_2.append(row["系列名称"])
    print(f"-- {'、 '.join(content_2)}")
    # 按长度判定是用等于还是用IN
    end_where: str
    if len(content_1) > 1:
        end_where = f"IN ({','.join(content_1)})"
    else:
        end_where = f"= {content_1[0]}"
    # 输出SQL
    # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
    print(f"UPDATE PRJ_TYPE_CONF SET PRJ_NAME = '{group_name}' WHERE PRJ_TYPE {end_where};")
