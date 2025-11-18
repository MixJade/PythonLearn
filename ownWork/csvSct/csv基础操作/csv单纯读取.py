# coding=utf-8
# @Time    : 2025/9/17 16:14
# @Software: PyCharm
import pandas as pd

data1 = pd.read_csv(r'待读取数据.csv')

# 保证列名相同
data1 = data1[['NAME', 'COMMENT', 'CATE']]

# 遍历data1中的每一行
for index1, row1 in data1.iterrows():
    print(f"name: {row1['NAME']} comment: {row1['COMMENT']}  cate: {row1['CATE']} ")
