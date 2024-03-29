# coding=utf-8
# @Time    : 2024/3/29 17:40
# @Software: PyCharm
import math


# 点坐标函数，输入是圆心的坐标、半径、与12点方向偏移的度数
def get_point(x, y, r, offset_degree):
    """计算圆与12点偏转特定角度的点坐标

    :param x: 圆心的横坐标
    :param y: 圆心的纵坐标
    :param r: 圆的半径
    :param offset_degree: 从12点方向偏移的角度
    """
    # 将偏移的度数转为弧度
    offset_rad = math.radians(offset_degree)

    # 计算偏移对应的坐标
    point_x = x + r * math.sin(offset_rad)
    point_y = y - r * math.cos(offset_rad)
    # 自动对结果进行四舍五入
    print(f'{point_x:.0f},{point_y:.0f}')


x1, y1 = 64, 64  # 圆心的点坐标
r1 = 62  # 圆的半径

# 测试我们的函数(五角星的五个点)
get_point(x1, y1, r1, 0)
get_point(x1, y1, r1, 2 * 72)
get_point(x1, y1, r1, 4 * 72)
get_point(x1, y1, r1, 72)
get_point(x1, y1, r1, 3 * 72)
