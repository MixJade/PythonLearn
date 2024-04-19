# coding=utf-8
# @Time    : 2024/4/19 16:30
# @Software: PyCharm
import re

# 正则表达式(匹配长度少于12字的行)
pattern1 = re.compile(r"^.{0,12}$")
# 正则表达式(匹配中文章节)
pattern2 = re.compile(r"第[一二三四五六七八九十百]+章")
# 正则表达式(匹配数字章节)
pattern3 = re.compile(r"第\d+章")
# 正则表达式(匹配连续空行)
pattern4 = re.compile(r"^\n+$")
