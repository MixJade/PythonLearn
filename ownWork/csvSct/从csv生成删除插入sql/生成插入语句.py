# coding=utf-8
# @Time    : 2024/3/7 17:43
# @Software: PyCharm
from datetime import datetime

import pandas as pd

# 输入的csv文件
inputFile = '待删除数据.csv'

# 读取CSV文件(如果读取失败，请手动将对应csv文件转为utf8格式)
df = pd.read_csv(inputFile, encoding='utf-8')

# 获取需要的列
df = df[['HOME_ID', 'DOG_TP', 'DOG_ID', '是否保留']]

# 逐行打印SQL语句，同时需要保留的数据不删
for index, row in df.iterrows():
    if row['是否保留'] == '保留':
        # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
        print(f"""
-- {row['HOME_ID']} {row['DOG_TP']} {row['DOG_ID']}
INSERT INTO HomeAndDog (relId, homeID, dogID, dogTP)
VALUES ('{datetime.now().strftime('%Y%m%d%H%M%S')}0{index + 1}',
       '{row['HOME_ID']}',
       '{row['DOG_TP']}',
       '{row['DOG_ID']}');
    """)
