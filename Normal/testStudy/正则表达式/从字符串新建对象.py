# coding=utf-8
# @Time    : 2024/2/1 16:53
# @Software: PyCharm
import re


class NiDot:
    def __init__(self, index: int, s_x: float, s_y: float):
        self.index = index
        self.s_x = s_x
        self.s_y = s_y

    def __repr__(self) -> str:
        return f'P{self.index}{self.s_x, self.s_y}'


def str_transfer_object_list(str_object: str) -> list[NiDot]:
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
        station1 = NiDot(index1, s_x1, s_y1)
        station_list.append(station1)
    return station_list


s = "[P1(3, 2), P3(5, 4), P4(4, 7), P7(7, 9), P15(7, 14), P17(6, 18)]"

print(str_transfer_object_list(s))
