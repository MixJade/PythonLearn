import pandas as pd
from utils.outFieldSQL import SqlParam, out_db_sql
from utils.convertCase import small_snake_to_camel

df = pd.read_csv('字段及对应注释.csv')
df = df[['NAME', 'COMMENT', 'LENGTH']]

sql_param_list: list[SqlParam] = []

for index, row in df.iterrows():
    sql_param_list.append(SqlParam(
        java_name=small_snake_to_camel(row["NAME"]),
        comment=row["COMMENT"],
        sql_field=row["NAME"].upper(),
        type_len=row["LENGTH"]
    ))

table_name = "STUDENT_INF"
table_comment = "学生表"

out_db_sql(sql_param_list, table_name, table_comment)
