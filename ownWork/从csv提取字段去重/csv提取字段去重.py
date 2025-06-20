# coding=utf-8
# @Time    : 2025/6/20 15:28
# @Software: PyCharm
import pandas as pd

df = pd.read_csv('有重复描述的字段.csv')
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
df_agg3_sorted = df_agg3.sort_values('dict')
# 确定以上的没问题之后，输出
for index, row in df_agg3_sorted.iterrows():
    print(f"""
    /**
     * {row["comment"]}
     * - {row["cate"]}
     * - {row["dict"]}
     */
    private String {row["field"]};""")
