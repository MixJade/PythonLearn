# coding=utf-8
# @Time    : 2025/9/17 16:14
# @Software: PyCharm
import pandas as pd

data1 = pd.read_csv(r'待读取数据.csv')[['NAME', 'COMMENT', 'CATE']]

# 只筛选某个的值
data2 = data1[data1['NAME'] == 'stuName']

print("\n筛选结果：")
print(data2)
