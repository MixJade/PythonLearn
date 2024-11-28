# coding=utf-8
# @Time    : 2021/6/13 12:27
# @Software: PyCharm
import csv
import re

from school.数学建模.间奏.前置1站点对象 import Station
from school.数学建模.间奏.间奏1路线对象保存 import LineInfo


def load_from_csv(filename: str) -> list[LineInfo]:
    """从csv加载路线数据

    :param filename: csv文件的路径
    :return: 路线列表对象
    """
    lines = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            line_num = int(row['路线编号'])
            total_len = int(row['路程(km)'])
            total_time = float(row['耗时(m)'])
            total_weight = float(row['载重(t)'])
            empty_spend = float(row['空载花费'])
            weight_spend = float(row['重载花费'])
            # 这里在解析站点列表
            the_stations = str_transfer_object_list(row['路线'])
            # 建立路线对象
            line = LineInfo(line_num, total_len, total_time, total_weight, empty_spend, weight_spend, the_stations)
            lines.append(line)
    return lines


def str_transfer_object_list(str_object: str) -> list[Station]:
    """将字符串转为特定对象

    :param str_object: 有对象基本信息的字符串，形如：P1(3, 2)
    :return: 转化后的list[NiDot]对象
    """
    station_list = []
    # 使用正则表达式匹配字符串中的所有P后面的内容
    # r表示原初字符串，意为：不需要转义符(防止因为斜杠被识别为转义符)
    for match in re.findall(r'P(\d+)\((\d+), (\d+)\)', str_object):
        index1, s_x1, s_y1 = map(int, match)
        # 使用匹配的内容创建Station对象，并添加到列表中
        station1 = Station(index1, 0, s_x1, s_y1)
        station_list.append(station1)
    return station_list


if __name__ == '__main__':
    line_info_list: list[LineInfo] = load_from_csv('../../A2兼收并蓄/题目一垃圾运输路线.csv')
    for line_info in line_info_list:
        print(line_info)
