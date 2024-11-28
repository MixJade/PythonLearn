# coding=utf-8
# @Time    : 2021/6/13 12:27
# @Software: PyCharm
from dataclasses import dataclass


@dataclass
class Station:
    """垃圾站站点对象"""
    index: int  # 站点编号
    s_t: float  # 站点垃圾装载量
    s_x: float  # 站点纵坐标
    s_y: float  # 站点横坐标

    def distance(self, station: 'Station') -> float:
        """返回当前站点到指定站点的距离

        这里单独抽一个方法，是因为有的题计算点与点的距离是按直线算。
        而我这道题按平行于坐标轴的路程算
        """
        return abs(self.s_x - station.s_x) + abs(self.s_y - station.s_y)

    def __repr__(self) -> str:
        """打印多个个对象所调用
        print(list[Station])
        """
        return f'P{self.index}{self.s_x, self.s_y}'  # 元组会自动加括号


def get_station_list() -> list[Station]:
    """得到37个垃圾站站点对象"""
    return [Station(1, 1.5, 3, 2),
            Station(2, 1.5, 1, 5),
            Station(3, 0.55, 5, 4),
            Station(4, 1.2, 4, 7),
            Station(5, 0.85, 0, 8),
            Station(6, 1.3, 3, 11),
            Station(7, 1.2, 7, 9),
            Station(8, 2.3, 9, 6),
            Station(9, 1.4, 10, 2),
            Station(10, 1.5, 14, 0),
            Station(11, 1.1, 17, 3),
            Station(12, 2.7, 14, 6),
            Station(13, 1.8, 12, 9),
            Station(14, 1.8, 10, 12),
            Station(15, 0.6, 7, 14),
            Station(16, 1.5, 2, 16),
            Station(17, 0.8, 6, 18),
            Station(18, 1.5, 11, 17),
            Station(19, 0.8, 15, 12),
            Station(20, 1.4, 19, 9),
            Station(21, 1.2, 22, 5),
            Station(22, 1.8, 21, 0),
            Station(23, 1.4, 27, 9),
            Station(24, 1.6, 15, 19),
            Station(25, 1.6, 15, 14),
            Station(26, 1, 20, 17),
            Station(27, 2, 21, 13),
            Station(28, 1, 24, 20),
            Station(29, 2.1, 25, 16),
            Station(30, 1.2, 28, 18),
            Station(31, 1.9, 5, 12),
            Station(32, 1.3, 17, 16),
            Station(33, 1.6, 25, 7),
            Station(34, 1.2, 9, 20),
            Station(35, 1.5, 9, 15),
            Station(36, 1.3, 30, 12),
            Station(37, 0, 0, 0)]


def get_some_lines(fun_index: int) -> list[list[int]]:
    """输出三种结果路径(1-网上的参考，2-原来的论文，3-现在的结果)"""
    # 1.从网上找的最短路径(它是从最远到原点)
    # 总路程:724km,总耗时:24.1h
    if fun_index == 1:
        return [[24, 18, 35, 7],
                [4],
                [30, 29, 27, 3],
                [33, 32, 22, 10],
                [8, 2],
                [28, 26, 21, 19, 14],
                [34, 17, 16, 6],
                [11],
                [36, 23, 15, 13],
                [25, 20, 31, 5],
                [12, 9, 1]]
    # 2.我原来论文的路径编号(从最远开始找，但当前点的横纵坐标不能大于上一个点)
    # 总路程:660km,总耗时:22.5h
    elif fun_index == 2:
        return [[30, 29, 27, 3],
                [28, 26, 32, 25, 5],
                [36, 23, 33, 21],
                [24, 18, 35, 15],
                [34, 17, 16, 2],
                [20, 11, 10],
                [19, 13, 8],
                [14, 7, 4, 1],
                [22],
                [12, 9],
                [31, 6]]
    # 3.我现在写的最短路径(从最近的点开始找)
    # 总路程:652km,总耗时:22.3h
    elif fun_index == 3:
        return [[1, 3, 4, 7, 15, 17],
                [2, 5, 6, 31],
                [9, 8, 13],
                [10, 12, 11],
                [16, 35, 18, 34],
                [22, 21, 33, 23],
                [14, 19, 25, 32],
                [20, 27, 26, 28],
                [24, 29, 30],
                [36]]


if __name__ == '__main__':
    station_data = get_station_list()
    # 第37个点是原点，且从列表删除这个点
    origin_dot = station_data.pop(36)
    # 三种不同的数据(1-网上的参考，2-原来的论文，3-现在的结果)
    all_line: list[list[int]] = get_some_lines(1)
    all_elements = [item for sublist in all_line for item in sublist]
    print("总共有元素: {}".format(len(all_elements)))
    print("有重复元素: {}".format(len(all_elements) != len(set(all_elements))))
    refer_total_length = 0  # 网上的总路程
    for one_line in all_line:
        # 加上第一个(最远点)到原点的路程
        refer_total_length += station_data[one_line[0] - 1].distance(origin_dot)
        # 加上最后一个(最近点)到原点的路程
        refer_total_length += station_data[one_line[-1] - 1].distance(origin_dot)
        # 加上每两个点(不包括原点)彼此之间的距离
        for i in range(1, len(one_line)):
            refer_total_length += station_data[one_line[i - 1] - 1].distance(station_data[one_line[i] - 1])
    refer_total_time = (refer_total_length * 60 / 40 + 36 * 10) / 60
    print(f"该方案的总路程:{refer_total_length}km,总耗时:{round(refer_total_time, 3)}h")
