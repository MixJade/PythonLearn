# coding=utf-8
# @Time    : 2024/11/7 22:27
# @Software: PyCharm


gua = [0, 0, 0, 0, 0, 0, 0, 0]
yao = [0, 0, 0, 0, 0, 0]

# 从100到999中取值
for i in range(100, 1000):
    # print(i)
    gua[i % 8] += 1
    yao[i % 6] += 1

print(gua)
print(yao)
