# coding=utf-8
# @Time    : 2024/3/30 10:35
# @Software: PyCharm
import pandas as pd

# 读取csv文件(如不存在，先执行 "测试生成csv.py")
df = pd.read_csv(r'../outputFile/train_data.csv')
print(df.head())

# 将csv转为feather(更快、压缩的数据文件)
df.to_feather('../outputFile/data.feather')

# 读取feather文件
df2 = pd.read_feather(r'../outputFile/data.feather')
print(df2.head())

# 将feather转为csv
df.to_csv('../outputFile/data.csv')
