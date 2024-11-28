# coding=utf-8
# @Time    : 2022/12/13 21:52
# @Software: PyCharm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
3、绘制饼状图(书P71)
读取“2022-12-1”日的国内新冠疫情数据，
统计大陆各省级单位'累计确诊','累计死亡','累计治愈' 三项各自总和
，然后绘制其饼状图，结果保存在当前目录，并命“饼状图.png”。
"""
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
plt.rcParams['axes.unicode_minus'] = False  # 设置正常显示符号
data_0 = pd.read_excel('../A1输入数据/data2022-12-01.xlsx', sheet_name=0)
data = data_0.drop(labels=[1, 3, 4])  # 删除港澳台
values = np.array(data)  # 数据转为np.array
p = plt.figure(figsize=(6, 6))  # 设画布为方，以得正圆
label = ['累计确诊', '累计死亡', '累计治愈']
explode = [0.01, 0.01, 0.01]  # 设定各项离心 n 个半径
plt.pie(sum(values[:, 1:4]), explode=explode, labels=label, autopct='%1.1f%%')  # 绘制饼图
plt.title('国家疫情饼状图', fontsize=20)
plt.savefig('../A2兼收并蓄/饼状图.png')  # 自定义路径
plt.show()
