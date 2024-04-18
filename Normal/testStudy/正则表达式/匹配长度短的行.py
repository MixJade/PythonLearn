# coding=utf-8
# @Time    : 2024/4/17 17:53
# @Software: PyCharm
import re


def find_matches(filename, pattern2):
    """输出文件中所有与某个正则表达式匹配的行
    """
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if pattern2.match(line):
                # 防止输出空行
                if line.strip():
                    print(line.strip())


# 正则表达式(匹配长度少于12字的行)
pattern1 = re.compile(r"^.{0,12}$")
# 调用函数，指定文件和正则表达式
find_matches(r'../../inputFile/文本处理/测试章节拆分.txt', pattern1)
