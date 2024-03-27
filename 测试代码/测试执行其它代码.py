# coding=utf-8
# @Time    : 2024/2/1 15:13
# @Software: PyCharm

"""
这里执行其它文件的代码，并更改其中的某些变量
"""
with open('测试被读取代码.py', 'r', encoding='utf-8') as file:
    code = file.read()

# 通过文本替换，修改code中的变量
code = code.replace('Original Value', 'newVariable')

# 执行修改后的代码
exec(code)
