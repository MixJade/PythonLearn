# coding=utf-8
# @Time    : 2025-01-08 11:16:07
# @Software: PyCharm

tableField: list[str] = []  # 表的字段列表
javaField: list[str] = []  # 代码的字段列表

with open('ibatis的更新列.txt', 'r') as file:
    for line in file:
        myField: list[str] = line.split("=")
        if len(myField) != 2:
            continue  # 不能通过等号均分成两组就说明不对
        tableField.append(myField[0].strip().upper())  # 结尾无逗号
        javaField.append(myField[1].strip())  # 除了最后一个元素，均以逗号结尾

# noinspection SqlNoDataSourceInspection
print("INSERT INTO XXX(")
for idx, val in enumerate(tableField):
    if idx == len(tableField) - 1:  # 如果索引等于列表长度减1，说明这是最后一个元素
        print(f"        {val}) VALUES (")
    else:
        print(f"        {val},")

for jf in javaField:
    print(f"     {jf}")
print(")")
