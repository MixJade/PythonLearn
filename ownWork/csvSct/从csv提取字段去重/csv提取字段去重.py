# coding=utf-8
# @Time    : 2025/6/20 15:28
# @Software: PyCharm
import pandas as pd
from utils.convertCase import camel_to_snake
from utils.genFieldXml import *

df = pd.read_csv('input/有重复描述的字段.csv')
df = df[['cate', 'dict', 'field', 'comment']]

# 开始去重(指定列)，保留第一次出现的重复行
df_unique2 = df.drop_duplicates(subset=['cate', 'dict', 'field'])

# 基于field列去重，同时聚合多列
df_agg3 = df_unique2.groupby('field').agg({
    'cate': lambda x: '、'.join(sorted(set(x))),  # 聚合时也顺便去重
    'dict': lambda x: '、'.join(sorted(set(x))),
    'comment': lambda x: '、'.join(sorted(set(x)))
}).reset_index()

# 按分类排序
df_agg3_sorted = df_agg3.sort_values('field').sort_values('dict')
# 添加一个新列
df_agg3_sorted['COLUMN_NAME'] = df_agg3_sorted['field'].apply(camel_to_snake)


"""生成字段的xml文件
"""
field_param_list: list[FieldParam] = []
for index, row in df_agg3_sorted.iterrows():
    # 添加字段内容
    field_param_list.append(FieldParam(
        code=row['COLUMN_NAME'],
        name=row['comment'],
        length=""  # 目前没有长度
    ))

gen_field_xml("../../xmlDeal/xml参照旧表字段/待新增的字段.xml", "STUDENT_INF", "学生表", field_param_list)