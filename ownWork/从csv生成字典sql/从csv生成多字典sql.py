# coding=utf-8
# @Time    : 2025/8/6 17:44
# @Software: PyCharm
import json

from utils.outDictSQL import DicMain, DicParam, out_hy_dic_sql, out_insert_dic_sql

# 读取JSON文件
with open("多字典及其码值.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 遍历每个分组并填入
dic_list: list[DicMain] = []
for dic_data in data:
    dic_code = dic_data["dicCode"]
    dic_name = dic_data["dicName"]
    # 字典起始排序,默认为0
    begin_seq = dic_data.get("beginSeq", 0)
    # 当起始序列为0时,是整个字典新增,否则默认是追加
    is_new = (begin_seq == 0)
    # 读取字典下的参数列表
    param_list = dic_data["parmList"]
    dic_param_list: list[DicParam] = []
    for index, param in enumerate(param_list):
        dic_param_list.append(DicParam(seq=index + begin_seq, code=param['code'], name=param['name']))
    dic_list.append(DicMain(code=dic_code, name=dic_name, is_new=is_new, parm_list=dic_param_list))

# 探查
print("\n-- " + "=" * 50)
for dic in dic_list:
    out_hy_dic_sql(dic, is_hy=False)
# 插入数据
print("\n-- " + "=" * 50)
for dic in dic_list:
    out_insert_dic_sql(dic)
# 核验
print("\n-- " + "=" * 50)
for dic in dic_list:
    out_hy_dic_sql(dic)
