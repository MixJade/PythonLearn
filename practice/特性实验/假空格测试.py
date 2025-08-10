# coding=utf-8
# @Time    : 2025/8/10 20:20
# @Software: PyCharm

"""在处理小说文件时，存在一种"假空格"
它有半个中文长，但不是真的空格
所以在处理文本缩进时非常有用，因为可以在所有地方显示“两个字长度的空格”
"""

# 正常的空格
print("    正常的空格    ".strip(" "))
# 假空格
line_tab = "　　"  # 特别的缩进符
print((line_tab + "假的空格" + line_tab).strip(" "))
