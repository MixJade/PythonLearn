# coding=utf-8
# @Time    : 2024/4/19 16:50
# @Software: PyCharm
import pandas as pd

# 读取两个csv文件
data1 = pd.read_csv(r'data/差异原表.csv')
data2 = pd.read_csv(r'data/差异子表.csv')

# 保证列相同
data1 = data1[['HOME_ID', 'HOME_NM', 'DOG_ID']]
data2 = data2[['HOME_ID', 'HOME_NM', 'DOG_ID']]

# 然后对两个文件进行合并，对特定列进行去重。得到的df3=df1-df2
data3 = pd.concat([data1, data2])
# subset后面传入列名，决定两个df是否相同的依据
data3 = data3.drop_duplicates(subset=['HOME_ID', 'DOG_ID'], keep=False)
print(f'两个文件不同的元素有{len(data3)}个')

# 通过求df1和df3的交集对df1进行去重
# 只在原表中存在表示需要给子表添加
only_in_data1 = pd.merge(data1, data3)
print(f'只在原表中的有{len(only_in_data1)}个')

# 通过求df2和df3的交集对df2进行去重
# 只在子表中存在表示需要删除
only_in_data2 = pd.merge(data2, data3)
print(f'只在子表中的有{len(only_in_data2)}个')

# 存储结果，使用index=0去除dataframe默认的行索引
only_in_data1.to_csv('需添加的数据结果.csv', index=False)
only_in_data2.to_csv('需删除的数据结果.csv', index=False)
print("差异文件已输出")
