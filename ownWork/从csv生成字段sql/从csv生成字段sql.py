import pandas as pd

df = pd.read_csv('字段及对应注释.csv')
df = df[['NAME', 'COMMENT']]

table_name = "STUDENT_INF"
table_comment = "学生表"

# 将NAME列的值用双引号包裹并聚合
name_result = ','.join([f"'{name.upper()}'" for name in df['NAME']])
# noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
print(f"""
-- 检查{table_comment}字段 预计0条
SELECT COLUMN_NAME
FROM USER_TAB_COLUMNS
WHERE TABLE_NAME = '{table_name}'
  AND COLUMN_NAME IN ({name_result});
""")

# 确定以上的没问题之后，输出SQL
print(f"-- {table_comment} 新增{len(df)}个字段")
for index, row in df.iterrows():
    # noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
    print(f"""-- {row["COMMENT"]}	{row["NAME"]}
ALTER TABLE {table_name} ADD {row["NAME"].upper()} VARCHAR2(3) NULL;
COMMENT ON COLUMN {table_name}.{row["NAME"].upper()} IS '{row["COMMENT"]}';""")

# noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
print(f"""
-- 核验{table_comment}字段 预计{len(df)}条
SELECT COLUMN_NAME
FROM USER_TAB_COLUMNS
WHERE TABLE_NAME = '{table_name}'
  AND COLUMN_NAME IN ({name_result});
""")

print("\n\n=========================Java实体类字段=============================")


def snake_to_camel(snake_str):
    """将小蛇形转为小驼峰
    :param snake_str: 形如 prj_name
    :return: prjName
    """
    components = snake_str.split('_')
    # 第一个单词保持小写，其余单词首字母大写
    return components[0] + ''.join(x.title() for x in components[1:])


table_name_con = table_name[0].upper() + table_name[1:].lower()
print(f"{snake_to_camel(table_name_con)}.java\n")
for index, row in df.iterrows():
    print(f'private String {snake_to_camel(row["NAME"])}; // {row["COMMENT"]}')

print("\n\n=========================ibatis的resultMap字段=============================")
for index, row in df.iterrows():
    print(f'<result property="{snake_to_camel(row["NAME"])}" column="{row["NAME"].upper()}" />')
