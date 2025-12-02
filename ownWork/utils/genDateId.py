# coding=utf-8
# @Time    : 2025/12/2 17:09
# @Software: PyCharm
from datetime import datetime


def get_time_id(i: int) -> str:
    """用当前时间打印时间戳，格式如2024030717275001

    :param i: 编号序列
    """
    now_time: str = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{now_time}0{i}"
