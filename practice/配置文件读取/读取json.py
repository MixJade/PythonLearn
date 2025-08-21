# coding=utf-8
# @Time    : 2025/8/21 10:21
# @Software: PyCharm
import json

# 读取JSON文件
with open("testRead/测试读取.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 遍历每个分组
for dic_data in data:
    dic_code = dic_data["dicCode"]
    dic_name = dic_data["dicName"]
    # 字典起始排序,默认为0
    begin_seq = dic_data.get("beginSeq", 0)

    print(f"\n字典编码: {dic_code}")
    print(f"字典名称: {dic_name}")
    print(f"起始序列: {begin_seq}")
    print("参数列表:")

    # 读取字典下的参数列表
    param_list = dic_data["parmList"]
    for index, param in enumerate(param_list):
        print(f"  code: {param['code']}, name: {param['name']}")
