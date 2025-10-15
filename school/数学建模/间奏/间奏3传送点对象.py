# coding=utf-8
# @Time    : 2021/6/13 12:27
# @Software: PyCharm
from 数学建模.间奏.间奏1路线对象保存 import LineInfo

# 铲车速度的倒数(分钟),本来是v=40公里/60分钟,倒数：1/v=60分钟/40公里
CAT_SPEED_RECIPROCAL: float = 60 / 40


class TransmitDot:
    """传送点
    每当铲车到传送点入口(离原点最远)，就消耗指定的时间，出现在传送点出口(离原点最近)
    """

    def __init__(self, line_info: LineInfo):
        self.index_num = line_info.lint_num
        self.begin_dot = line_info.the_stations[-1]
        self.end_dot = line_info.the_stations[0]
        # 花费的时间需要重新算，因为路线的耗时算上了往返路程
        transmit_time = 0
        # 每个垃圾站都会耗时10分钟
        transmit_time += len(line_info.the_stations) * 10
        # 算上彼此之间的距离
        for i in range(len(line_info.the_stations) - 1):
            _distance = line_info.the_stations[i].distance(line_info.the_stations[i + 1])
            transmit_time += _distance * CAT_SPEED_RECIPROCAL
        self.spend_time = transmit_time

    def __str__(self) -> str:
        """打印单个对象调用"""
        return (f"传送点{self.index_num}:"
                f"起{self.begin_dot.s_x, self.begin_dot.s_y},"
                f"终{self.end_dot.s_x, self.end_dot.s_y},"
                f"耗时{self.spend_time}m")

    def __repr__(self) -> str:
        """打印多个对象调用"""
        return f"线路{self.index_num}"
