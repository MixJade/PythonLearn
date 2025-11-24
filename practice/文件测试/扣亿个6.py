# coding=utf-8
# @Time    : 2024/3/27 9:27
# @Software: PyCharm

"""为了测试压缩算法的原理,将一亿个六输出成txt文件
输出的txt文件:97657KB(约95MB)
压缩成zip文件:96KB
"""
with open("../outputFile/zip炸弹文件.txt", "w") as f:
    f.write("6" * 1_0000_0000)
