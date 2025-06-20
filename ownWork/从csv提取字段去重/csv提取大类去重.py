# coding=utf-8
# @Time    : 2025/6/20 17:46
# @Software: PyCharm
import pandas as pd

df = pd.read_csv('有重复描述的字段.csv')
df = df[['cate', 'code', 'dict']]

# 开始去重(指定列)，保留第一次出现的重复行
df_unique2 = df.drop_duplicates(subset=['cate', 'code', 'dict'])
# 输出switch代码
print('\n\nswitch (distributeCode) {')
for index, row in df_unique2.iterrows():
    print(f'  case "{row["code"]}": // {row["cate"]} {row["dict"]}\n    return "特殊表单";')
print('}')

# 输出sql代码
print("\n\n")
begin_seq = 3
for index, row in df_unique2.iterrows():
    begin_seq += 1
    # noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
    print(f'''insert into DICT (key_nm, code, name, seq)
values ('CODE', '{row["cate"]}', '{row["dict"]}', '{begin_seq}');''')

# 基于field列去重，同时聚合多列
df_agg3 = df_unique2.groupby('cate').agg({
    'code': lambda x: ','.join(sorted(set(x)))
}).reset_index()
# 输出类别代码
print("\n\n")
for index, row in df_agg3.iterrows():
    print(f'// {row["cate"]}')
    print(f'Code = ", ,{row["code"]}";')
