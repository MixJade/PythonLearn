# coding=utf-8
# @Time    : 2024/10/2 10:40
# @Software: PyCharm

"""
找出一个列表中所有的重复项，并输出，
比如元组列表[(2, 1, 0), (3, 2, 2), (2, 1, 3), (4, 5, 1), (5, 9, 1), (3, 3, 0)]
输出一组结果(只校验前两个是否相等)
[[(2, 1, 0), (2, 1, 3)]]
"""
tuples = [(2, 1, 0), (3, 2, 2), (2, 1, 3), (4, 5, 1), (5, 9, 1), (3, 3, 0)]
dicts = {}
for item in tuples:
    key = item[:2]  # 只考虑元组的前两个元素
    if key in dicts:
        dicts[key].append(item)
    else:
        dicts[key] = [item]

duplicates = [value for value in dicts.values() if len(value) > 1]
print(duplicates)
