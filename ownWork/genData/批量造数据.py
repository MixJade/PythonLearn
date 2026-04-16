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


def gen_rel_id(idx: int) -> str:
    now_time: str = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{now_time}0{idx + 1}"


dog_names: list[str] = [
    "旺财", "富贵", "骨头",
]

# 逐行打印SQL语句
for i, item in enumerate(dog_names, start=1):
    # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
    print(f"""INSERT INTO HomeAndDog (relId,relNo, homeID, dogID, dogTP, dogNm)
VALUES ('{gen_rel_id(i)}','{generate_unique_number()}', '121', '211', '2', '{item}');
""")
