import pandas as pd

# 读取CSV文件(如果读取失败，请将对应csv文件转为utf8格式)
df = pd.read_csv('PROJ_INFO.csv')
df = df[['PRJ_ID', 'PROJ_NAME']]
# print(df)
# 读取CSV文件(如果读取失败，请将对应csv文件转为utf8格式)
df2 = pd.read_csv('项目对应规则名称.csv')
df2 = df2[['PROJ_NAME', 'PROJ_RULE']]
# print(df2)
prjName = []
for index, row in df2.iterrows():
    prjName.append(row["PROJ_NAME"])

print(prjName)

# 连接两张表
df2 = df2.merge(df, on='PROJ_NAME', how='left')
# print(df2)
# 查看找不到的系列名称
# print("以下项目没有对应的项目系列号")
for index, row in df2.iterrows():
    if pd.isnull(df2.loc[index, 'PRJ_ID']):
        print(row["PROJ_NAME"])

# 确定以上的没问题之后，输出SQL
for index, row in df2.iterrows():
    # noinspection SqlResolve,SqlNoDataSourceInspection
    print(f"""
-- {row["PROJ_NAME"]}	{row["PROJ_RULE"]}
UPDATE PROJ_INFO
SET PROJ_RULE = '{row["PROJ_RULE"]}'
WHERE PRJ_ID = '{row["PRJ_ID"]}'
  AND PROJ_NAME = '{row["PROJ_NAME"]}';""")
