# coding=utf-8
# @Time    : 2024/4/17 17:53
# @Software: PyCharm
import re


def find_matches(filename, pattern):
    """输出文件中所有与某个正则表达式匹配的行
    """
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if pattern.match(line):
                # 防止输出空行
                if line.strip():
                    print(line.strip())


# 正则表达式(匹配长度少于12字的行)
pattern1 = re.compile(r"^.{0,12}$")
# 正则表达式(匹配中文章节)
pattern2 = re.compile(r"第[一二三四五六七八九十百]+章")
# 正则表达式(匹配数字章节)
pattern3 = re.compile(r"第\d+章")
# 正则表达式(匹配连续空行)
pattern4 = re.compile(r"^\n+$")
# 调用函数，指定文件和正则表达式
find_matches(r'../../inputFile/文本处理/测试章节拆分.txt', pattern1)
