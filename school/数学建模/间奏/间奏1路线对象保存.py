# coding=utf-8
# @Time    : 2021/6/13 12:27
# @Software: PyCharm
import csv

from 数学建模.间奏.前置1站点对象 import Station


class LineInfo:
    """
    间奏：建立一个路线对象
    """

    def __init__(self, lint_num: int, total_len: float, total_time: float, total_weight: float,
                 empty_spend: float, weight_spend: float,
                 the_stations: list[Station]) -> None:
        self.lint_num = lint_num
        self.total_len = round(total_len, 3)
        self.total_time = round(float(total_time), 3)
        self.total_weight = round(float(total_weight), 3)
        self.empty_spend = round(float(empty_spend), 3)
        self.weight_spend = round(float(weight_spend), 3)
        self.total_spend = round(float(empty_spend + weight_spend), 3)
        self.the_stations = the_stations

    def __str__(self) -> str:
        """打印单个对象"""
        return f"Line{self.lint_num}: 总路程{self.total_len}km, 耗时{self.total_time}分,载重{self.total_weight}t, " \
               f"空载花费{self.empty_spend}元,重载花费{self.weight_spend}元, 总花费{self.total_spend}元," \
               f"经过站点{self.the_stations}"

    def __repr__(self) -> str:
        """打印多个对象"""
        return f"{self.lint_num}号线(耗时{int(self.total_time)}m)"


def save_to_csv(lines: list[LineInfo], filename: str) -> None:
    """将路线数据写入csv

    :param lines: 路线列表对象
    :param filename: 保存csv文件的路径
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['路线编号', '路程(km)', '耗时(m)', '载重(t)',
                      '空载花费', '重载花费', '总花费', '路线']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for line in lines:
            writer.writerow({
                '路线编号': str(line.lint_num),
                '路程(km)': str(line.total_len),
                '耗时(m)': str(line.total_time),
                '载重(t)': str(line.total_weight),
                '空载花费': str(line.empty_spend),
                '重载花费': str(line.weight_spend),
                '总花费': str(line.total_spend),
                '路线': str(line.the_stations),
            })
        print("csv文件保存成功")
