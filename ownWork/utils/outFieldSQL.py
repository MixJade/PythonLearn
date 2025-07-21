# coding=utf-8
# @Time    : 2025/7/21 15:56
# @Software: PyCharm
from typing import NamedTuple
from utils.convertCase import snake_to_big_camel


class SqlParam(NamedTuple):
    """SQL填入参数(name,comment,field,type_len)
    """
    java_name: str  # 实体类中字段名称,形如:prjName
    comment: str  # 字段注释,形如:项目名称
    sql_field: str  # SQL字段名称,形如:PRJ_NAME
    type_len: str  # SQL类型+长度,形如:VARCHAR2(3)


def out_db_sql(param_list: list[SqlParam], table_name, table_comment):
    # 将field列用双引号包裹并聚合
    field_result = ", ".join(f"'{param.sql_field}'" for param in param_list)
    # noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
    print(f"""
-- 检查{table_comment}字段 预计0条
SELECT COLUMN_NAME
FROM USER_TAB_COLUMNS
WHERE TABLE_NAME = '{table_name}'
  AND COLUMN_NAME IN ({field_result});
""")

    # 确定以上的没问题之后，输出SQL
    print(f"-- {table_comment} 新增{len(param_list)}个字段")
    for row in param_list:
        # noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
        print(f"""-- {row.comment}	{row.java_name}
ALTER TABLE {table_name} ADD {row.sql_field} {row.type_len} NULL;
COMMENT ON COLUMN {table_name}.{row.sql_field} IS '{row.comment}';""")

    # noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
    print(f"""
-- 核验{table_comment}字段 预计{len(param_list)}条
SELECT COLUMN_NAME
FROM USER_TAB_COLUMNS
WHERE TABLE_NAME = '{table_name}'
  AND COLUMN_NAME IN ({field_result});
""")

    print("\n\n=========================Java实体类字段=============================")

    table_name_con = table_name[0].upper() + table_name[1:].lower()
    print(f"{snake_to_big_camel(table_name_con)}.java\n")
    for row in param_list:
        print(f'private String {row.java_name}; // {row.comment}')

    print("\n\n=========================ibatis的resultMap字段=============================")
    for row in param_list:
        print(f'<result property="{row.java_name}" column="{row.sql_field}" />')
