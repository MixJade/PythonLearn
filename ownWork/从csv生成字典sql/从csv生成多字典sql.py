# coding=utf-8
# @Time    : 2025/8/6 17:44
# @Software: PyCharm
from typing import NamedTuple

import pandas as pd


class DicParam(NamedTuple):
    seq: int
    code: str
    name: str


class DicMain(NamedTuple):
    code: str
    name: str
    parm_list: list[DicParam]


# 请替换成你的 CSV 文件路径
csv_file_path = r'多字典及其码值.csv'
# 读取 CSV 文件
df = pd.read_csv(csv_file_path)
df = df[['DIC_CODE', 'DIC_NAME', 'PARM_CODE', 'PARM_NAME']]

# 按照 DIC_CODE 列进行分组
grouped = df.groupby('DIC_CODE')

# 遍历每个分组并填入
dic_list: list[DicMain] = []
for group_name, group_data in grouped:
    a_dic_group = group_data.reset_index()
    dic_name = a_dic_group.iloc[0]['DIC_NAME']  # 获取第一个元素的字典名称
    dic_param_list: list[DicParam] = []
    for index, row in a_dic_group.iterrows():
        dic_param_list.append(DicParam(seq=index, code=row['PARM_CODE'], name=row['PARM_NAME']))
    dic_list.append(DicMain(code=group_name, name=a_dic_group.iloc[0]['DIC_NAME'], parm_list=dic_param_list))

# 遍历每个分组
print("\n-- " + "=" * 50)
for dic in dic_list:
    # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
    print(f"""
-- 检查字典·{dic.name} 预计0条
SELECT *
FROM PARM_DIC
WHERE KEY_NAME = '{dic.code}';""")

# 插入数据
print("\n-- " + "=" * 50)
for dic in dic_list:
    print(f"\n-- 插入字典·{dic.name} 共计{len(dic.parm_list)}条")
    for parm in dic.parm_list:
        # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
        print(f"""INSERT INTO PARM_DIC (KEY_NAME, OPT_CODE, OPT_NAME, SEQN, STS)
VALUES ('{dic.code}', '{parm.code}', '{parm.name}', {parm.seq}, '1');""")

print("\n-- " + "=" * 50)
for dic in dic_list:
    # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
    print(f"""
-- 检查字典·{dic.name} 预计{len(dic.parm_list)}条
SELECT *
FROM PARM_DIC
WHERE KEY_NAME = '{dic.code}';""")
