# coding=utf-8
# @Time    : 2021/6/13 12:27
# @Software: PyCharm
import math

from 数学建模.间奏.前置1站点对象 import get_station_list
from 数学建模.间奏.间奏1路线对象保存 import LineInfo, save_to_csv

'''第一题：运输车调度方案
由于每个垃圾站的垃圾量和坐标不变，所以重载费用(按"吨+公里"算钱)是不变的；
为了使总运输费用最少，就要使空载费用最少，即运输路程最少；
此处使用dijkstra算法，先找最短路径，再找次短的
由若干个点组成一条线路。
'''
station_data = get_station_list()
# 第37个点是原点，且从列表删除这个点
origin_dot = station_data.pop(36)
# 每辆车最大装载6t
MAX_CAT_CAPACITY: float = 6
# 最多平均工作4小时
MAX_AVERAGE_TIME: float = 4 * 60
# 最长工作时间5小时(平均4小时，假设最多5小时)
MAX_SPEND_TIME: float = 5 * 60
# 汽车速度的倒数(分钟),本来是v=40公里/60分钟,倒数：1/v=60分钟/40公里
CAT_SPEED_RECIPROCAL: float = 60 / 40
# 最终路径集合
result_lines = []
"""
一、先算出所需的路线
"""
while station_data:
    # 路径存储
    one_line = []
    # 最短路径算法:找出下一个最近的点，一直到垃圾车装满
    cat_capacity = 0  # 每条路线的车容量
    now_station = origin_dot  # 当前车所在的地点
    one_way_journey = 0  # 单次行程(点对点的路程)
    now_spend_time = 0  # 预计耗时(临时变量，按最多的算)
    while True:
        # 从剩下的站点中找到距离当前站点最短的
        mini_dot_distance = float('inf')  # 当前点到其它点的最短距离(默认正无穷)
        future_station = origin_dot  # 将要去的下一个站点
        for station in station_data:
            # 下一站到当前站的距离
            next_dot_distance = station.distance(now_station)
            # 下一站到当前站的花费时间(算上往返、装货)这个没必要，因为不会超
            next_spend_time = now_spend_time + next_dot_distance * 2 * CAT_SPEED_RECIPROCAL + 10
            # 下一站将有的装载量
            next_cat_capacity = cat_capacity + station.s_t
            if ((mini_dot_distance >= next_dot_distance)
                    and (next_cat_capacity <= MAX_CAT_CAPACITY)
                    and (next_spend_time <= MAX_SPEND_TIME)):
                mini_dot_distance = next_dot_distance
                future_station = station
        # 找出最短站点后，进行处理，没找到就进入下一次循环
        if mini_dot_distance == float('inf'):
            break
        else:
            one_way_journey += mini_dot_distance  # 加上点对点的路程
            one_line.append(future_station)  # 路线加上这个最短的点
            # 时间统计加上预计耗时
            now_spend_time += now_station.distance(future_station) * 2 * CAT_SPEED_RECIPROCAL + 10
            now_station = future_station  # 当前站变为下一个站
            cat_capacity += future_station.s_t  # 当前车装上下一个站的垃圾
            station_data.remove(future_station)  # 从候选站移除该站
    result_lines.append((one_line, cat_capacity, one_way_journey))

"""
二、计算每条路径的花费、时间
"""
line_info_list: list[LineInfo] = []
for _index, result_line in enumerate(result_lines):
    empty_cost = 0  # 空载花费
    weight_cost = 0  # 重载花费
    now_station = origin_dot  # 从原点开始算
    for station in result_line[0]:
        # 空车跑到最远的点，在返程过程中装垃圾
        weight_cost += 1.8 * station.s_t * station.distance(origin_dot)
    # 该路径的路程(单次行程+直接到终点的路程)
    the_line_len = result_line[2] + result_line[0][-1].distance(origin_dot)
    # 该路径消耗时间(路程*速度的倒数=时间，+每个站点的装货时间)
    the_line_time = the_line_len * CAT_SPEED_RECIPROCAL + len(result_line[0]) * 10
    empty_cost += 0.4 * the_line_len
    line_info_list.append(
        LineInfo(_index + 1, the_line_len, the_line_time, result_line[1], empty_cost, weight_cost, result_line[0]))

# 依次输出每条线路的信息，并进行统计
all_len, all_spend, all_time, all_weight = 0, 0, 0, 0
for line_info in line_info_list:
    print(line_info)
    all_len += line_info.total_len
    all_spend += line_info.total_spend
    all_time += line_info.total_time
    all_weight += line_info.total_weight

print(f"总路程:{all_len}km,总花费{all_spend}元,总耗时{round(all_time / 60, 3)}h,总重量{round(all_weight, 3)}t")

# 间奏：将计算出的路线保存在csv中
save_to_csv(line_info_list, '../A2兼收并蓄/题目一垃圾运输路线.csv')

"""
三、通过贪心算法计算运输车的路线
"""


def distribute_tasks(task_list: list[LineInfo], truck_count1: int) -> list[int]:
    """贪心算法分配任务

    :param task_list: 任务耗时列表
    :param truck_count1: 运输车的数量
    :return: 分配后，每个运输车的工作时间
    """
    # 从大到小排序
    sorted_tasks = bubble_sort(task_list)
    print("按耗时排序后的路线：", sorted_tasks)
    # 创建一个长度为“工作人数”的数组，每个人当前工作时间为0
    worker_times = [0] * truck_count1
    # 任务数组，包含6个空列表的列表,用于区分是那些任务
    task_time_group = [[] for _ in range(len(worker_times))]
    # 从耗时最长的任务开始，将其分配给当前工作时间最小的人
    for task in sorted_tasks:
        # min_worker_index是工作时长最小的运输车的索引
        min_worker_index = worker_times.index(min(worker_times))
        worker_times[min_worker_index] += task.total_time
        task_time_group[min_worker_index].append(task)
    print("分配的任务组为：")
    for _index2, task_group in enumerate(task_time_group):
        print(f"  第{_index2 + 1}辆车,路线:{task_group},"
              f"总时长:{convert(sum(a_task.total_time for a_task in task_group))}")
    return worker_times


def bubble_sort(origin_task: list[LineInfo]) -> list[LineInfo]:
    """冒泡排序法，返回耗时从大到小的路线序列

    :param origin_task: 原始的路线(任务时长)列表
    :return: 从大到小的路线(任务时长)列表
    """
    n = len(origin_task)
    for i in range(n):
        for j in range(0, n - i - 1):
            if origin_task[j].total_time < origin_task[j + 1].total_time:
                origin_task[j], origin_task[j + 1] = origin_task[j + 1], origin_task[j]
    return origin_task


def convert(minutes: float) -> str:
    """将175.0，给输出成2小时45分"""
    # 一小时有 60 分钟
    hours: int = int(minutes // 60)  # 双斜线表示向下取整
    minutes: int = int(minutes % 60)
    return f"{hours}h{minutes}m"


# 计算需要几辆车(总工作时间/平均工作时间)
truck_count: int = math.ceil(all_time / MAX_AVERAGE_TIME)
print(f"一共需要{truck_count}辆运输车")
# 通过贪心算法为这些车分配路线
print("最终每辆车的工作时长", distribute_tasks(line_info_list, truck_count))
