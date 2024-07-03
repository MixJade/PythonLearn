# coding=utf-8
# @Time    : 2024/7/3 15:23:42
# @Software: PyCharm
from pprint import pprint

point_lst = [{'Name': '田辛', 'Age': 40, 'Points': [80, 20]}, {'Name': '张三', 'Age': 20, 'Points': [90, 10]},
             {'Name': '李四', 'Age': 30, 'Points': [70, 30]}]

# pprint可以格式化的输出json,比较美观
# 一般情况下默认的就够用了
print("\n=====一、默认的输出======\n")
pprint(point_lst)

# 可以指定宽度,超出宽度的会换行
print("\n=====二、指定宽度输出======\n")
pprint(point_lst, width=40)

# 可以指定最大深度，当嵌套到一定程度时会省略
print("\n=====三、指定最大深度======\n")
pprint(point_lst, depth=1)
pprint(point_lst, depth=2)

# 可以指定缩进,对于嵌套的元素,其元素会有缩进
print("\n=====四、指定缩进======\n")
pprint(point_lst, indent=4)
pprint(point_lst[0], width=4, indent=4)

# 可以设置紧凑输出(主要对有大量元素的列表有用)
print("\n=====五、紧凑输出======\n")
pprint(list(range(1000000, 1000020)), compact=True)
