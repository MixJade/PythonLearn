# coding=utf-8
# @Time    : 2025/6/30 11:09
# @Software: PyCharm
import pandas as pd

df = pd.read_csv('input/有重复描述的字段.csv')
df = df[['cate', 'dict', 'field', 'comment']]

# 开始去重(指定列)，保留第一次出现的重复行
df_unique2 = df.drop_duplicates(subset=['cate', 'dict', 'field'])

# 分组输出
groups = df_unique2.groupby('cate')
grouped_list = [group for _, group in groups]

# 查看结果
for i, group in enumerate(grouped_list):
    print("\n" + "-" * 30)
    print(f"分组 {i + 1}:")
    print(group)
    print("-" * 30)

    # 基于field列去重，同时聚合多列
    df_agg5 = group.groupby('field').agg({
        'dict': lambda x: '、'.join(sorted(set(x))),
        'comment': lambda x: '、'.join(sorted(set(x)))
    }).reset_index()

    # 确定以上的没问题之后，输出
    for index, row in df_agg5.iterrows():
        print(
            f'myMap.put("{row["field"]}", myDto.get{row["field"][0].upper() + row["field"][1:]}());//{row["comment"]}')
