# coding=utf-8
# @Time    : 2024/3/9 18:13
# @Software: PyCharm

# 1.下划线分割大数字，输出是正常的
print('\n1.下划线分割大数字，输出是正常的')
a: int = 1_000_000_000
print(f"{a}")

# 2.输出下划线分割的数字
print('\n2.输出下划线分割的数字(千位分割)')
b: float = 1e9  # 科学计数法
print(f"{b:_}")
print(f"{b:,}")

# 3.自动格式化float小数位数
print('\n3.自动保留float小数位数')
c: float = 123.45678
print(f"{c:.2f}")
print(f"{c:.0f}")

# 3.1 补充：自动填充数字
print('\n3.1 补充：自动填充数字')
cc: int = 12
# 至少三位，不足部分用0补齐
print(f"{cc:03d}")

# 4.设置对齐格式
print('\n4.设置对齐格式')
mar_var: str = "默认的左对齐"
print(f"{mar_var :<20}")
print(f"{'以及居中对齐' :^20}")
print(f"{'还有右对齐' :>20}")

# 5.设置对齐填充文本
print('\n5.设置对齐填充文本')
print(f"{mar_var :_<20}")
print(f"{'以及居中对齐' :#^20}")
print(f"{'还有右对齐' :|>20}")

# 6.以及自动填充算式
print('\n6.以及自动填充算式')
d, e = 3, 5
print(f"{d + e = }")
print(f"{bool(e) = }")

# 7.输出大括号
print('\n7.输出大括号')
print(f"这是大括号{{{bool(e) = }，以及另一个括号}}")
