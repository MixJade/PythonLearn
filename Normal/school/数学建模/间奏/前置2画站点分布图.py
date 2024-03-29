# coding=utf-8
# @Time    : 2021/6/13 12:27
# @Software: PyCharm
import matplotlib.pyplot as plt

from school.数学建模.间奏.前置1站点对象 import get_station_list

station_data_list = get_station_list()
# 获取每个点的横坐标和纵坐标
x_values = [item.s_x for item in station_data_list]
y_values = [item.s_y for item in station_data_list]
# 指定默认字体(防止中文乱)
plt.rcParams['font.sans-serif'] = 'SimHei'
# 设置正常显示符号
plt.rcParams['axes.unicode_minus'] = False
# 设定散点图的标题并加上轴标签
plt.title('37个站点分布')
plt.xlabel('x')
plt.ylabel('y')
# 画散点图
plt.scatter(x_values, y_values, marker='o')
# 加上格子线
plt.grid(True)
# 为每个点加上文本
for sd in station_data_list:
    plt.text(sd.s_x, sd.s_y, f"P{sd.index}({sd.s_x},{sd.s_y})")

plt.savefig('../../A2兼收并蓄/垃圾站分布图.png')  # 自定义路径
plt.show()  # 展示散点图
