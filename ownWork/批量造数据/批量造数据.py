# coding=utf-8
# @Time    : 2024/3/7 17:43
# @Software: PyCharm
from datetime import datetime

# 逐行打印SQL语句
for i in range(0, 1000):
    # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
    print(f"""INSERT INTO HomeAndDog (relId, homeID, dogID, dogTP)
VALUES ('{datetime.now().strftime('%Y%m%d%H%M%S')}0{i}', '121', '211', '2');
    """)
