# coding=utf-8
# @Time    : 2025/7/21 15:01
# @Software: PyCharm
import pandas as pd

from utils.convertCase import snake_to_camel

# 读取两个csv文件
data1 = pd.read_csv(r'拟回灌字段.csv')
data2 = pd.read_csv(r'拟新增字段.csv')

# 需新增字段的表
table_name = "STUDENT_INF"
table_comment = "学生表"

# 保证列相同
data1 = data1[['NAME', 'COMMENT', 'LENGTH']]
data2 = data2[['CATE', 'NAME', 'COMMENT', 'LENGTH']]

# 在data2中新增IS_BACK和LENGTH两列
data2['IS_BACK'] = 'N'

# 标记data1中哪些行被匹配到
data1['IS_MATCHED'] = 'N'

# 遍历data2中的每一行
for index2, row2 in data2.iterrows():
    comment2 = row2['COMMENT']
    if row2['LENGTH'] is None:
        data2.at[index2, 'LENGTH'] = 'VARCHAR2(255)'
    # 检查data1中是否有相同的COMMENT
    for index1, row1 in data1.iterrows():
        comment1 = row1['COMMENT']
        if comment2 == comment1:
            data2.at[index2, 'IS_BACK'] = 'Y'
            data2.at[index2, 'LENGTH'] = row1['LENGTH']
            data2.at[index2, 'NAME'] = snake_to_camel(row1['NAME'])
            data1.at[index1, 'IS_MATCHED'] = True
            break

# 筛选出data1中未被匹配的数据
unmatched_data1 = data1[data1['IS_MATCHED'] == 'N'].drop(columns=['IS_MATCHED'])

# 输出data1中未被匹配的数据
print("\n未被匹配的data1数据:")
print(unmatched_data1)

# 导出为csv
data2[['CATE', 'NAME', 'COMMENT', 'IS_BACK', 'LENGTH']].to_csv(
    '新增的字段_结果.csv',
    index=False,
    encoding='utf-8-sig'
)
print("\n\nCSV 文件:【新增的字段_结果.csv】已生成！")
