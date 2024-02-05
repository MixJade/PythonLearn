# coding=utf-8
# @Time    : 2022/11/29 21:52
# @Software: PyCharm
import numpy as np

"""
1、创建数组并进行运算
（1）创建一个数值范围为0～1,间隔为0.01的数组（大小：10×10）。
（2）创建100个服从正态分布的随机数数组（大小：10×10）。
（3）对创建的两个数组进行四则运算。
（4）对创建的随机数组进行简单的统计分析。
"""
# 1
print("\n====================================")
arr_1 = np.arange(0, 1, 0.01).reshape(10, 10)
print("1.创建一个数值范围为0～1,间隔为0.01的数组")
print(arr_1)
# 2.
print("\n====================================")
arr_2 = np.random.randn(10, 10)
print("2.创建100个服从正态分布的随机数数组（大小：10×10）")
print(arr_2)
# 3.
print("\n====================================")
print("3.对创建的两个数组进行四则运算")
print("加法运算", arr_1 + arr_2)
print("减法运算", arr_1 - arr_2)
print("乘法运算", arr_1 * arr_2)
print("除法运算", arr_1 / arr_2)
# 4.
# 排序
print("\n====================================")
print("4.对创建的随机数组进行简单的统计分析")
arr_1.sort(axis=1)
print("对数组1排序(沿横轴)\n", arr_1)
arr_1.sort(axis=0)
print("对数组1排序(沿纵轴)\n", arr_1)
# 去重
# print('去重后的数组为:\n', np.unique(arr_1))
# 利用统计函数进行分析
print('数组的和为：', np.sum(arr_1))  # 计算数组的和
print('数组横轴的和为：', arr_1.sum(axis=0))  # 沿着横轴计算求和
print('数组纵轴的和为：', arr_1.sum(axis=1))  # 沿着纵轴计算求和
print('数组的均值为：', np.mean(arr_1))  # 计算数组均值
print('数组横轴的均值为：', arr_1.mean(axis=0))  # 沿着横轴计算数组均值
print('数组纵轴的均值为：', arr_1.mean(axis=1))  # 沿着纵轴计算数组均值
print('数组的标准差为：', np.std(arr_1))  # 计算数组标准差
print('数组的方差为：', np.var(arr_1))  # 计算数组方差
print('数组的最小值为：', np.min(arr_1))  # 计算数组最小值
print('数组的最大值为：', np.max(arr_1))  # 计算数组最大值
print('数组的最小元素为：', np.argmin(arr_1))  # 返回数组最小元素的索引
print('数组的最大元素为：', np.argmax(arr_1))  # 返回数组最大元素的索引
print('数组元素的累计和为：', np.cumsum(arr_1))  # 计算所有元素的累计和
print('数组元素的累计积为：\n', np.cumprod(arr_1))  # 计算所有元素的累计积
