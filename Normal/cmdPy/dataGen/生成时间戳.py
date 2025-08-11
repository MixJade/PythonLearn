# coding=utf-8
# @Time    : 2024/3/7 16:57
# @Software: PyCharm
from datetime import datetime


def get_time_id(num: int) -> None:
    """用当前时间打印时间戳，格式如2024030717275001

    :param num: 需要打印的时间戳数量
    """
    for i in range(num):
        now_time: str = datetime.now().strftime('%Y%m%d%H%M%S')
        print(f"{now_time}0{i + 1}")


# 打印时间戳
get_time_id(3)
