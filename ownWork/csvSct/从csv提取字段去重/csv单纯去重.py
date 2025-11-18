# coding=utf-8
# @Time    : 2025/7/8 17:45
# @Software: PyCharm
import pandas as pd

# dtype指定读取格式，防止字符串被读取为数字
df = pd.read_csv('input/需去重的字典.csv', dtype={'码值': str})
df = df[['名称', '码值']]

# 开始去重(指定列)，保留第一次出现的重复行
df_unique2 = df.drop_duplicates(subset=['码值'])

# 确定以上的没问题之后，输出
for index, row in df_unique2.iterrows():
    print(f'meMap.put("{row["码值"]}", "{row["名称"]}");')
