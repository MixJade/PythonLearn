# coding=utf-8
# @Time    : 2021/6/13 12:27
# @Software: PyCharm
"""第三题:8吨运输车调度
这里题目说有载重量为 4 吨、 6 吨、 8 吨三种运输车，
但并没有其它限制条件，故只需要按照8吨运输车算即可。
只需要将第一题的6改成8，以及保存的csv文件名改一下即可
"""

with open('题目1运输车调度方案.py', 'r', encoding='utf-8') as file:
    code = file.read()

# 通过文本替换，修改code中的变量
code = code.replace('MAX_CAT_CAPACITY: float = 6', 'MAX_CAT_CAPACITY: float = 8')
code = code.replace('题目一垃圾运输路线.csv', '题目三8吨运输车路线.csv')

# 执行修改后的代码
exec(code)
