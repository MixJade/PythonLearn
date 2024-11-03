# coding=utf-8
# @Time    : 2022/11/29 21:52
# @Software: PyCharm
import numpy as np

"""
2、创建一个国际象棋的棋盘
（1）创建一个8*8的矩阵。
（2）把这个矩阵与国际象棋棋盘黑格对应的位置为1，白格对应的位置为0。
"""
# （1）创建一个8*8矩阵。
arr = np.zeros((8, 8))
# （2）把这个矩阵与国际象棋棋盘黑格对应的位置为1，白格对应的位置为0。
arr[0:7:2, 0:7:2] = 1  # 这个2是步长
arr[1:8:2, 1:8:2] = 1
print(arr)
# 变成棋盘
for i in range(8):
    for j in range(8):
        if arr[i][j] == 1:
            print("■", end='  ')
        else:
            print("□", end='  ')
    print()
