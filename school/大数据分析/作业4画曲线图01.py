# coding=utf-8
# @Time    : 2022/12/13 21:52
# @Software: PyCharm
import unittest

import matplotlib.pyplot as plt
import numpy as np


class AttemptOne(unittest.TestCase):
    """Matplotlib绘图(书P54):
    掌握Matplotlib的绘图基本语法
    """

    def test_draw_a_curve(self):
        draw_a_curve()
        self.skipTest("画y=x^2曲线")

    def test_draw_sin_cos(self):
        draw_two_sin_cos()
        self.skipTest("画两幅图，Sin与Cos曲线")

    def test_draw_two_img(self):
        draw_two_img()
        self.skipTest("画两幅图且挨在一起")


if __name__ == '__main__':
    unittest.main()


def draw_a_curve() -> None:
    """练手：画两条y=x^2、y=x^4曲线
    """
    data = np.arange(0, 1.1, 0.01)
    plt.title('lines')  # 添加标题
    plt.xlabel('x')  # 添加x轴的名称
    plt.ylabel('y')  # 添加y轴的名称
    plt.xlim((0, 1))  # 确定x轴范围
    plt.ylim((0, 1))  # 确定y轴范围
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1])  # 规定x轴刻度
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1])  # 确定y轴刻度
    plt.plot(data, data ** 2)  # 添加y=x^2曲线
    plt.plot(data, data ** 4)  # 添加y=x^4曲线
    plt.legend(['y=x^2', 'y=x^4'])
    plt.savefig('../A2兼收并蓄/y=x^2.jpg')  # 自定义路径
    plt.show()


def draw_two_sin_cos() -> None:
    """
    1、Matplotlib 绘图
    画布中包含两个子图，第一幅子图绘制Sin曲线，第二副子图绘制Cos曲线，
    x轴的范围是0~4π，最后存放在当前目录下，存储的文件名为Sin-Cos.png
    """
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    plt.rcParams['axes.unicode_minus'] = False  # 设置正常显示符号
    rad = np.arange(0, np.pi * 4, 0.01)  # 设置圆周率范围
    p1 = plt.figure(figsize=(8, 6), dpi=80)  # 确定画布大小
    # 创建一个2行1列的子图，并开始绘制第一幅
    p1.add_subplot(2, 1, 1)
    plt.title('sin曲线')  # 添加标题
    plt.xlabel('rad')  # 添加x轴的名称
    plt.ylabel('value')  # 添加y轴的名称
    plt.xlim((0, np.pi * 4))  # 确定x轴范围
    plt.ylim((-1, 1))  # 确定y轴范围
    # 规定x轴刻度
    plt.xticks([0, np.pi / 2, np.pi, np.pi * 1.5, np.pi * 2, np.pi * 2.5, np.pi * 3, np.pi * 3.5, np.pi * 4])
    plt.yticks([-1, -0.5, 0, 0.5, 1])  # 确定y轴刻度
    plt.plot(rad, np.sin(rad))  # 添加sin(x)曲线
    plt.legend(['y=sin(x)'])
    # 开始绘制第二幅
    p1.add_subplot(2, 1, 2)
    plt.title('cos曲线')  # 添加标题
    plt.xlabel('rad')  # 添加x轴的名称
    plt.ylabel('value')  # 添加y轴的名称
    plt.xlim((0, np.pi * 4))  # 确定x轴范围
    plt.ylim((-1, 1))  # 确定y轴范围
    # 规定x轴刻度
    plt.xticks([0, np.pi / 2, np.pi, np.pi * 1.5, np.pi * 2, np.pi * 2.5, np.pi * 3, np.pi * 3.5, np.pi * 4])
    plt.yticks([-1, -0.5, 0, 0.5, 1])  # 确定y轴刻度
    plt.plot(rad, np.cos(rad))  # 添加cos(x)曲线
    plt.legend(['y=cos(x)'])
    plt.tight_layout()  # 调整两个子图间距
    plt.savefig('../A2兼收并蓄/Sin-Cos.png')  # 自定义路径
    plt.show()


def draw_two_img():
    """同时画两张图"""
    rad = np.arange(0, np.pi * 2, 0.01)
    # 第一幅子图
    p1 = plt.figure(figsize=(8, 6), dpi=80)  # 确定画布大小
    # 创建一个2行1列的子图，并开始绘制第一幅
    ax1 = p1.add_subplot(2, 1, 1)
    plt.title('lines')  # 添加标题
    plt.xlabel('x')  # 添加x轴的名称
    plt.ylabel('y')  # 添加y轴的名称
    plt.xlim((0, 1))  # 确定x轴范围
    plt.ylim((0, 1))  # 确定y轴范围
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1])  # 规定x轴刻度
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1])  # 确定y轴刻度
    plt.plot(rad, rad ** 2)  # 添加y=x^2曲线
    plt.plot(rad, rad ** 4)  # 添加y=x^4曲线
    plt.legend(['y=x^2', 'y=x^4'])
    # 第二幅子图
    ax2 = p1.add_subplot(2, 1, 2)  # 开始绘制第二幅
    plt.title('sin & cos(x)')  # 添加标题
    plt.xlabel('rad')  # 添加x轴的名称
    plt.ylabel('value')  # 添加y轴的名称
    plt.xlim((0, np.pi * 2))  # 确定x轴范围
    plt.ylim((-1, 1))  # 确定y轴范围
    plt.xticks([0, np.pi / 2, np.pi, np.pi * 1.5, np.pi * 2])  # 规定x轴刻度
    plt.yticks([-1, -0.5, 0, 0.5, 1])  # 确定y轴刻度
    plt.plot(rad, np.sin(rad))  # 添加sin(x)曲线
    plt.plot(rad, np.cos(rad))  # 添加cos(x)曲线
    plt.legend(['y=sin(x)', 'y=cos(x)'])
    plt.tight_layout()  # 调整两个子图间距
    plt.savefig('../A2兼收并蓄/sincos.jpg')  # 自定义路径
    plt.show()
