import numpy as np
from numpy import linalg
import pandas as pd

data = [[0.697, 0.460, 1],
        [0.774, 0.376, 1],
        [0.634, 0.264, 1],
        [0.608, 0.318, 1],
        [0.556, 0.215, 1],
        [0.430, 0.237, 1],
        [0.481, 0.149, 1],
        [0.437, 0.211, 1],
        [0.666, 0.091, 0],
        [0.243, 0.267, 0],
        [0.245, 0.057, 0],
        [0.343, 0.099, 0],
        [0.639, 0.161, 0],
        [0.657, 0.198, 0],
        [0.360, 0.370, 0],
        [0.593, 0.042, 0],
        [0.719, 0.103, 0]]
column = ['密度', '含糖', '好瓜']
dataSet = pd.DataFrame(data, columns=column)
# 数据的初步转化与操作--属性x变量2行17列数组，并添加一组1作为吸入的偏置x^=（x;1）
x = np.array([dataSet['密度'].values, dataSet['含糖'].values, \
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
y = np.array([1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
# 定义初始参数
beta = np.array([[0], [0], [1]])  # β列向量
old_l = 0  # 3.27式l值的记录，这是上一次迭代的l值
n = 0

while 1:
    beta_T_x = np.dot(beta.T[0], x)
    # 对β进行转置取第一行（因为β转置后是array([[0, 0, 1]]，取第一行得到array([0, 0, 1])
    # ，再与x相乘（dot）,beta_T_x表示β转置乘以x)
    cur_l = 0  # 当前的l值
    for i in range(17):
        cur_l = cur_l + (-y[i] * beta_T_x[i] + np.log(1 + np.exp(beta_T_x[i])))
        # 计算当前3.27式的l值，这是目标函数，希望他越小越好
    # 迭代终止条件
    if np.abs(cur_l - old_l) <= 0.000001:  # 精度，二者差在0.000001以内就认为可以了，说明l已经很收敛了
        break  # 满足条件直接跳出循环

    # 牛顿迭代法更新β
    # 求关于β的一阶导数和二阶导数
    n = n + 1
    old_l = cur_l
    dbeta = 0
    d2beta = 0
    for i in range(17):
        dbeta = dbeta - np.dot(np.array([x[:, i]]).T,
                               (y[i] - (np.exp(beta_T_x[i]) / (1 + np.exp(beta_T_x[i])))))  # 一阶导数
        d2beta = d2beta + np.dot(np.array([x[:, i]]).T,
                                 np.array([x[:, i]]).T.T) * (np.exp(beta_T_x[i])
                                                             / (1 + np.exp(beta_T_x[i]))) * (
                             1 - (np.exp(beta_T_x[i]) / (1 + np.exp(beta_T_x[i]))))
    beta = beta - np.dot(linalg.inv(d2beta), dbeta)
print('模型参数是：', beta)
print('迭代次数：', n)
