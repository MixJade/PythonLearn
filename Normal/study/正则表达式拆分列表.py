# coding=utf-8
# @Time    : 2024/11/25 21:35
# @Software: PyCharm
import re

# 列表和正则表达式
lst = ['a', 'b', 'c', '1', 'd', 'e', '2', 'f', 'g', 'h']
pattern = '[0-9]'

# 初始化临时列表和结果列表
temp = []
res = []

# 遍历原始列表
for i in lst:
    # 如果元素符合正则表达式
    if re.match(pattern, i):
        # 如果临时列表不为空，将临时列表添加到结果列表
        if temp:
            res.append(temp)
            temp = []
    # 将元素添加到临时列表
    temp.append(i)

# 将最后的临时列表添加到结果列表
if temp:
    res.append(temp)

# 打印结果列表
print(res)

# 输出结果：[['a', 'b', 'c', '1'], ['d', 'e', '2'], ['f', 'g', 'h']]
