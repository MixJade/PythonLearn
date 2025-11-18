# coding=utf-8
# @Time    : 2025-01-08 11:16:07
# @Software: PyCharm
from utils.ibatisOut import IBatisParam, out_insert_col

param_list: list[IBatisParam] = []

with open('ibatis更新列.txt', 'r') as file:
    for line in file:
        myField: list[str] = line.split("=")
        if len(myField) != 2:
            continue  # 不能通过等号均分成两组就说明不对
        param_list.append(IBatisParam(
            java_field=myField[1].replace("#", "").replace(",", "").strip(),
            sql_column=myField[0].strip().upper())
        )

# 更新列变插入列
out_insert_col(param_list, False)
