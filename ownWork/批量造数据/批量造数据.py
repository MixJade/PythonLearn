# coding=utf-8
# @Time    : 2024/3/7 17:43
# @Software: PyCharm
from datetime import datetime
import random

NUMBER_LENGTH = 12
LOWER_BOUND = 10 ** (NUMBER_LENGTH - 1)  # 12位数的最小值
UPPER_BOUND = 10 ** NUMBER_LENGTH - 1  # 12位数的最大值
generated_numbers: list = []


def generate_unique_number():
    """生成随机数
    :return: 随机数(可以带前缀)
    """
    while True:
        number = random.randint(LOWER_BOUND, UPPER_BOUND)
        if number not in generated_numbers:
            generated_numbers.append(number)
            return f"Ran{number}"


# 逐行打印SQL语句
for i in range(1, 1001):
    # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
    print(f"""INSERT INTO HomeAndDog (relId,relNo, homeID, dogID, dogTP)
VALUES ('{datetime.now().strftime('%Y%m%d%H%M%S')}{i:04d}',{generate_unique_number()}, '121', '211', '2');
    """)
