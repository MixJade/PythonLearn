# coding=utf-8
# @Time    : 2025/9/17 16:32
# @Software: PyCharm
import pandas as pd

data1 = pd.read_csv(r'待读取数据.csv')[['NAME', 'COMMENT', 'CATE']]

# 1. 新增列
data1['IS_BACK'] = 'N'
data1['LENGTH'] = None
print("\npandas新增列")
print(data1)

# 2. 删除列
data1 = data1.drop(columns=['COMMENT'])
print("\npandas删除列")
print(data1)

# 3. 列聚合
# 直接使用str.join()
result1 = "、".join(data1["NAME"])
print("\n直接聚合结果")
print(result1)
# 给每个元素加双引号后用逗号连接
result2 = ", ".join([f"'{item}'" for item in data1["NAME"]])
print("\n给每个元素加双引号后用逗号连接")
print(result2)
