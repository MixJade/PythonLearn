# coding=utf-8
# @Time    : 2024/1/31 15:13
# @Software: PyCharm
"""
现在有十个任务，
每个工作任务的时长是[138, 94, 96, 99, 136, 148, 139, 175, 177, 136]，
我需要将这10个任务分给6个人，
我希望他们每个人的工作时间尽可能地平均，且耗时最多不能超过300
"""


def distribute_tasks(task_list: list[int], worker_count1: int) -> list[int]:
    """贪心算法分配任务

    :param task_list: 任务耗时列表
    :param worker_count1: 工作者的数量
    :return: 分配后，每个工作者的工作时间
    """
    # 从大到小排序
    sorted_tasks = bubble_sort(task_list)
    print("排序后的任务列表：", sorted_tasks)
    # 创建一个长度为“工作人数”的数组，每个人当前工作时间为0
    worker_times = [0] * worker_count1
    # 任务数组，包含6个空列表的列表,用于区分是那些任务
    task_time_group = [[] for _ in range(len(worker_times))]
    # 从耗时最长的任务开始，将其分配给当前工作时间最小的人
    for task in sorted_tasks:
        # - `min(worker_times)`返回`worker_times`中的最小值。
        # - `worker_times.index(...)`返回括号中元素在`worker_times`列表中第一次出现的索引位置。
        min_worker_index = worker_times.index(min(worker_times))
        worker_times[min_worker_index] += task
        task_time_group[min_worker_index].append(task)
    print("分配的任务组为：", task_time_group)
    return worker_times


def bubble_sort(origin_task: list[int]) -> list[int]:
    """冒泡排序法，返回从大到小的任务序列

    :param origin_task: 原始的任务时长列表
    :return: 从大到小的任务时长列表
    """
    n = len(origin_task)
    for i in range(n):
        for j in range(0, n - i - 1):
            if origin_task[j] < origin_task[j + 1]:
                origin_task[j], origin_task[j + 1] = origin_task[j + 1], origin_task[j]
    return origin_task


# 十个任务， 每个任务的时长
task_lengths = [138, 94, 96, 99, 136, 148, 139, 175, 177, 136]
# 6个劳动者
worker_count = 6
print("最终每个人的工作时长", distribute_tasks(task_lengths, worker_count))
