# coding=utf-8
# @Time    : 2025/4/7 10:43
# @Software: PyCharm
import pandas as pd

# 加载报文字段数据(无表头)
message_fields = pd.read_csv('报文字段.csv', names=['报文字段', '描述'], header=None)
# 加载字段映射数据(无表头)
field_mappings = pd.read_csv('字段映射.csv', names=['映射字段', '描述', '报文字段'], header=None)

# 将报文字段和字段映射数据转换为字典
message_fields_dict = message_fields.set_index('报文字段')['描述'].to_dict()
field_mappings_dict = field_mappings.set_index('报文字段')['映射字段'].to_dict()
print()  # 换行
# 遍历报文
for key, value in message_fields_dict.items():
    if key in field_mappings_dict:
        print(f"    private String {field_mappings_dict.get(key)};       // {value}")
    else:
        print(f"    private String {key};       // {value}")
