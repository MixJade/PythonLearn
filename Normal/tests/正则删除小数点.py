# coding=utf-8
# @Time    : 2024/4/11 17:18
# @Software: PyCharm
import re

# 删除所有的"."后面的数字,遇到符号或空格则不删
s = "M908.1 353.1l-253.9-36.9L540.7"
new_str = re.sub(r'\.\d+', '', s)
print(new_str)
