# coding=utf-8
# @Time    : 2024/4/19 16:50
# @Software: PyCharm
import pandas as pd

# 读取两个csv文件
data1 = pd.read_csv(r'旧数据.csv')[['CHECK_ID', 'SCENE']]
data2 = pd.read_csv(r'新数据.csv')[['CHECK_ID', 'SCENE']]

# 将新数据转为字典
df2_dict = data2.set_index('CHECK_ID')['SCENE'].to_dict()

print('\n--- 检查数据变动')
for index1, row1 in data1.iterrows():
    check_id = row1['CHECK_ID']
    scene = row1['SCENE']
    if (check_id in df2_dict) and (df2_dict[check_id] != scene):
        print(f"update: {check_id} {scene} ————> {df2_dict[check_id]}")

# 然后对两个文件进行合并，对特定列进行去重。得到的df3=df1-df2
data3 = pd.concat([data1, data2])
# subset后面传入列名，决定两个df是否相同的依据
data3 = data3.drop_duplicates(subset=['CHECK_ID'], keep=False)

# 通过求df1和df3的交集对df1进行去重
only_in_data1 = pd.merge(data1, data3)
print(f'\n--- 检查删除数据 {len(only_in_data1)}条')
for index1, row3 in only_in_data1.iterrows():
    print(f"delete: {row3['CHECK_ID']} {row3['SCENE']}")

# 通过求df2和df3的交集对df2进行去重
only_in_data2 = pd.merge(data2, data3)
print(f'\n--- 检查新增数据 {len(only_in_data2)}条')
for index1, row3 in only_in_data2.iterrows():
    print(f"add: {row3['CHECK_ID']} {row3['SCENE']}")
