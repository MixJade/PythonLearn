# coding=utf-8
# @Time    : 2026/6/8 15:43
# @Software: PyCharm

import json

json_file_path = r'desFormControl.json'

print(f"读取文件: {json_file_path}\n")

# 读取JSON文件
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 打印Markdown表格表头
print("| 表单项 | 绑定属性 | 字典项 |")
print("|---|---|---|")

# 遍历数据并打印表格行
for item in data:
    form_field_describe = item.get('formFieldDescribe', '')
    bound_property = item.get('boundProperty', '')
    general_dictionary = item.get('generalDictionary', '')

    # 处理可能的空值
    form_field_describe = form_field_describe if form_field_describe else '-'
    bound_property = bound_property if bound_property else '-'
    general_dictionary = general_dictionary if general_dictionary else '-'

    print(f"| {form_field_describe} | {bound_property} | {general_dictionary} |")

print()
print(f"共 {len(data)} 条记录")
