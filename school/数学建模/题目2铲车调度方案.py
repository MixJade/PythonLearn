# coding=utf-8
# @Time    : 2021/6/13 12:27
# @Software: PyCharm
from 数学建模.间奏.前置1站点对象 import Station
from 数学建模.间奏.间奏2路线对象读取 import load_from_csv
from 数学建模.间奏.间奏3传送点对象 import TransmitDot

'''第二题：铲车调度方案
由于运输车的路线已经确定，故应让铲车等运输车。
且每条路线耗时已确定，不妨将第一题的十条线路看做十个传送点。
每当铲车到传送点入口(离原点最远)，就消耗指定的时间，出现在传送点出口(离原点最近)。
先不考虑“铲车到下一条路线入口时，运输车还没有到”这种情况，只让铲车从一个节点到另一个节点。
等铲车方案出了以后，再建立一个铲车、运输车的时刻表，来对各车辆的出发时间进行统筹
'''

line_info_list = load_from_csv('../A2兼收并蓄/题目一垃圾运输路线.csv')
# 传送点列表(这里的传送耗时需要重新算，因为原路线耗时包括了往返路程)
transmit_dot_list: list[TransmitDot] = []
# 将路线变成传送点
for line_info in line_info_list:
    transmit_dot_list.append(TransmitDot(line_info))

"""
前置、公共的配置
"""
# 汽车速度的倒数(分钟),本来是v=40公里/60分钟,倒数：1/v=60分钟/40公里
CAT_SPEED_RECIPROCAL: float = 60 / 40
# 原点对象，用于计算距离
origin_dot = Station(37, 0, 0, 0)
# 最长工作时间6小时(假设夜间运输)
MAX_SPEND_TIME: float = 6 * 60


def get_expected_time(now_end_dot: Station, next_transmit_dot: TransmitDot) -> float:
    """获取耗时期望

    :param now_end_dot: 当前传送点的出口
    :param next_transmit_dot: 下一个传送点
    :return: 到下一个点+回家的时间
    """
    to_next_start = now_end_dot.distance(next_transmit_dot.begin_dot)
    next_end_to_origin = next_transmit_dot.end_dot.distance(origin_dot)
    return (to_next_start + next_end_to_origin) * CAT_SPEED_RECIPROCAL + next_transmit_dot.spend_time


"""一、初步计算(实际没算铲车等待运输车的时间)
从原点出发，先找期望耗时最少的点，接着找次少的。
每次选择传送点时，先判断从该传送点返回是否超时。
如果接下来所有的传送点都会超时，则直接回城
"""
forklift_index = 0
while transmit_dot_list:
    forklift_index += 1
    # 设置本次循环的初始值
    now_dot = origin_dot
    already_speed_time = 0
    # 本次循环是为了找一台铲车的路线
    forklift_line: list[TransmitDot] = []
    while True:
        # 从剩余传送点中，找到耗时期望最少的点
        fut_tran_dot: TransmitDot | None = None
        mini_expected_time: float = float('inf')
        for transmit_dot in transmit_dot_list:
            expected_time = get_expected_time(now_dot, transmit_dot)
            # 当前期望+已经耗时>最大时长，则跳过这个点
            if expected_time + already_speed_time > MAX_SPEND_TIME:
                continue
            # 当前期望<目前最小期望，那当前期望就是最小期望
            if expected_time <= mini_expected_time:
                fut_tran_dot = transmit_dot
                mini_expected_time = expected_time
        # 最后看有没有找到期望的点
        if fut_tran_dot is None:
            # 没有期望的点说明这铲车完成使命了
            already_speed_time += now_dot.distance(origin_dot) * CAT_SPEED_RECIPROCAL
            print(f"第{forklift_index}台铲车耗时{int(already_speed_time)}m", end=',')
            break
        else:
            # 有期望的点还能再努力一下，先加上时间
            already_speed_time += now_dot.distance(fut_tran_dot.begin_dot) * CAT_SPEED_RECIPROCAL
            already_speed_time += fut_tran_dot.spend_time
            # 再到下一个传送点的终点
            now_dot = fut_tran_dot.end_dot
            # 将期望点添加到列表
            forklift_line.append(fut_tran_dot)
            transmit_dot_list.remove(fut_tran_dot)
    # 打印一台铲车的路线
    print(f"铲车路线{forklift_index}:{forklift_line}")
