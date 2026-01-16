# coding=utf-8
# @Time    : 2026/1/16 16:36
# @Software: PyCharm

"""
这里的表名通过`show tables`命令获取
"""
txt_file_path = "show tables表名.txt"

tab_names = []
with open(txt_file_path, "r", encoding="utf-8") as file:
    for line in file:
        if "" != line:
            tab_name = line.strip()
            tab_names.append(tab_name)

# 提前获取最后一个元素的索引
last_index = len(tab_names) - 1
# 输出sql
for index, tab_name in enumerate(tab_names):
    # noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
    print(f"SELECT '{tab_name}' AS table_name, COUNT(*) AS row_count FROM {tab_name}", end="")
    if index == last_index:
        print(";")
    else:
        print(" UNION ALL")
