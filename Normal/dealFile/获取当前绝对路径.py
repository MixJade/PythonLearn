# coding=utf-8
# @Time    : 2024/3/8 15:11
# @Software: PyCharm
import os

# 获取当前Py文件的绝对路径
print("当前文件所在文件夹:", os.getcwd())

# 获取当前Py文件上二级文件夹的绝对路径
path = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))

print("当前文件上二级文件夹:", path)
