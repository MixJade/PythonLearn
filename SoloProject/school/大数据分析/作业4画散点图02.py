# coding=utf-8
# @Time    : 2022/12/13 21:52
# @Software: PyCharm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
2、绘制散点图(书P59)
读取“2022-12-1”日的国内新冠疫情数据，
绘制大陆各省级单位‘累计死亡’、‘累计确诊增量’、‘累计治愈增量’的散点图，
结果保存在当前目录，并命名为“散点图.png”。
"""

plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
plt.rcParams['axes.unicode_minus'] = False  # 设置正常显示符号
data_0 = pd.read_excel('../A1输入数据/data2022-12-01.xlsx', sheet_name=0)
data = data_0.drop(labels=[1, 3, 4])  # 删除港澳台，变成31省份
values = np.array(data)  # 数据转为np.array
arr1 = np.array(range(31))  # 现有31个省份，就有31个横坐标
# 开始画图
plt.figure(figsize=(8, 7))  # 设置画布
plt.xlabel('省份')
plt.ylabel('人数(千)')
# 散点图一:累计确诊
plt.scatter(arr1, list(values[:, 1] / 1000), marker='D', c='blue')
# 散点图二:累计死亡
plt.scatter(arr1, list(values[:, 2] / 1000), marker='o', c='red')
# 散点图三:'累计治愈
plt.scatter(arr1, list(values[:, 3] / 1000), marker='v', c='green')
plt.xticks(arr1, values[:, 0], rotation=90)  # rotation=90即旋转90度
plt.legend(['累计确诊', '累计死亡', '累计治愈'])  # 设置图例
plt.title('新冠12-01散点图')  # 添加图表标题
plt.savefig('../A2兼收并蓄/散点图.png')  # 自定义路径
plt.show()
