# coding=utf-8
# @Time    : 2025/11/5 17:34
# @Software: PyCharm
import pandas as pd

# 1. 读取CSV文件
df = pd.read_csv("查到的字典.csv", encoding="utf-8")

# 有时key被自动识别为number类型，可以这样将索引强制转为字符串
df["KEY"] = df["KEY"].astype(str)  # 强制 KEY 列为 str

# 2. 以第一列作为键、第二列作为值生成字典
result_dict = df.set_index("KEY")["VALUE"].to_dict()

# 3. 打印结果
print("生成的字典（可直接粘贴在python使用）：")
print(result_dict)
