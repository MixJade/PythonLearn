# coding=utf-8
# @Time    : 2025/6/23 20:39
# @Software: PyCharm
import pandas as pd

# 读取CSV文件
df = pd.read_csv('生成的字段.csv')
df = df[['COLUMN_NAME', 'comment', 'cate', 'dict']]
# 读取CSV文件
df2 = pd.read_csv('input/SYS_USER_TAB_COLUMNS.csv')
df2 = df2[['COLUMN_NAME', 'DATA_TYPE', 'DATA_LENGTH']]
# 读取第二个CSV文件
df3 = pd.read_csv('input/SYS_USER_TAB_COLUMNS_2.csv')  # 替换为实际文件名
df3 = df3[['COLUMN_NAME', 'DATA_TYPE', 'DATA_LENGTH']]
combined_df = pd.concat([df2, df3], ignore_index=True)  # 合并两个DataFrame
df2 = combined_df.drop_duplicates(subset=['COLUMN_NAME'])  # 基于COLUMN_NAME去重（保留第一个出现的记录）

# 连接两张表
df = df.merge(df2, on='COLUMN_NAME', how='left')
for index, row in df.iterrows():
    data_type = 'VARCHAR2(200)'
    if pd.isnull(df.loc[index, 'DATA_TYPE']):
        print("-- 暂无可参考字段")
    else:
        data_type = f'{row["DATA_TYPE"]}({int(row["DATA_LENGTH"])})'
    # noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
    print(f"""-- {row["comment"]}({row["cate"]})({row["dict"]})
ALTER TABLE MY_TABLE
ADD {row["COLUMN_NAME"]} {data_type} NULL;
COMMENT ON COLUMN MY_TABLE.{row["COLUMN_NAME"]} IS '{row["comment"]}';""")
