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

print("100-999中除8时，0-7余数为：")
print(gua)
print("100-999中除6时，0-5的余数为：")
print(yao)
