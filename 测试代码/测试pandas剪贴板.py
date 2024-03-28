# coding=utf-8
# @Time    : 2024/3/28 11:21
# @Software: PyCharm
import pandas as pd

"""Pandas自带将文本插入剪贴板的功能
"""
df = pd.DataFrame(["Text to copy"])
df.to_clipboard(index=False, header=False)
