# coding=utf-8
# @Time    : 2025/6/20 15:28
# @Software: PyCharm
import pandas as pd
from utils.convertCase import camel_to_snake

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
# 确定以上的没问题之后，输出
for index, row in df_agg3_sorted.iterrows():
    print(f"""
    /**
     * {row["comment"]}
     * - {row["cate"]}
     * - {row["dict"]}
     */
    private String {row["field"]};""")

# 生成添加字段的csv
print("\n" + ("=" * 100) + "\n")
# 添加一个新列
df_agg3_sorted['COLUMN_NAME'] = df_agg3_sorted['field'].apply(camel_to_snake)

# 临时重命名并导出
df_agg3_sorted[['COLUMN_NAME', 'comment', 'cate', 'dict']].to_csv(
    '生成的字段.csv',
    index=False,
    encoding='utf-8-sig'
)

print("CSV 文件已生成！")
