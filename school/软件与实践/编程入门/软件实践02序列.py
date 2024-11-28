# coding=utf-8
# @Time    : 2021/11/9 16:30
# @Software: PyCharm
import random
import unittest
from functools import reduce

import numpy


class AttemptTwo(unittest.TestCase):

    def test_question_1(self):
        """输出指定 m，n 之间所有的素数"""
        expected = 5
        result = out_prime_number(5, 30)
        self.assertIn(expected, result)

    def test_question_2(self):
        random_and_list_merge()
        self.skipTest("使用random与列表合并")

    def test_question_3(self):
        input_str_to_list()
        self.skipTest("列表添加，输入exit退出")

    def test_question_4(self):
        """去除列表中相邻且重复元素"""
        expected = [1, 2, 3, 4, 5, 6, 8, 12, 13]
        li02 = [1, 2, 3, 4, 4, 4, 4, 4, 4, 5, 6, 6, 8, 8, 12, 12, 12, 12, 13, 13]
        result = remove_list_repeat(li02)
        print("去重结果：", result)
        self.assertEqual(expected, result)

    def test_question_5(self):
        """使用map,reduce,filter处理数字序列"""
        expected = 420
        li01 = [1, 3, 6, 8, 10, 11, 17]
        result = three_array_api(li01)
        self.assertEqual(expected, result)

    def test_question_6(self):
        """读取文件，分割单词，化为字典"""
        # r意为：原始字符串，可以防止识别到转义字符
        list1 = read_file_to_list(r'../../A1输入数据/zen.txt')
        result = mimic_dict(list1)
        print(result)
        self.assertIn("python", result)  # python在最终字典的key中


if __name__ == '__main__':
    unittest.main()


def out_prime_number(m: int, n: int) -> list[int]:
    """输出指定 m，n 之间所有的素数"""
    result: list[int] = []
    if m > n:
        m, n = n, m
    for i in range(m, n + 1):
        if i == 1:
            continue
        tem = 1
        for j in range(2, i):  # 判断素数
            if i % j == 0:
                tem = 0
                break
        if tem == 1:
            print(i, "is prime number")
            result.append(i)
    return result


def random_and_list_merge() -> None:
    """使用random与列表合并"""
    ball_red_list = range(1, 34)
    ball_blue_list = range(1, 17)
    num_red = random.sample(ball_red_list, 6)
    num_blue = random.sample(ball_blue_list, 1)
    print("红球:", num_red)
    print("蓝球:", num_blue)
    print("最终结果：", num_red + num_blue)


def input_str_to_list() -> None:
    """列表添加，输入exit退出"""
    string_list = []
    print("输入字符放入列表，输入exit终止")
    while 1:
        temp = input("请输入字符串：")
        if temp == 'exit':
            break
        string_list.append(temp)
    print("最终列表：\n", string_list)


# 创建一个函数，遍历去除给定列表中中相邻且重复的元素(只保留一个)后，打印输出结果。
# 说明：输入参数为 l1=[1,2,3,4,4,4,4,4,4,5,6,6,8,8,12,12,12,12,13,13]，操作后，
# 保证原有整体排序不变，仅处理相邻且重复的元素
def remove_list_repeat(li01):
    """去除列表中相邻且重复元素"""
    length = len(li01)
    temp = li01[0]
    i = 1
    while i < length:
        if temp == li01[i]:
            li01.remove(li01[i])
            length -= 1
        else:
            temp = li01[i]
            i = i + 1
    return li01


# 第五题
# 请仅使用map,reduce,filter依次进行如下三次操作(使用匿名函数)
def three_array_api(li01: list[int]) -> int:
    """使用map,reduce,filter处理数字序列
    from functools import reduce"""
    # a.剔除掉所有的偶数后打印;
    li01 = list(filter(lambda x: x % 2 == 1, li01))  # 使用匿名函数
    print("剔除掉所有的偶数后", li01)
    # b.对剩下的数字每个数字进行平方后打印;
    li01 = list(map(lambda x: x ** 2, li01))  # 使用匿名函数
    print("对剩下的数字每个数字进行平方后打印", li01)
    # c.对数组求和后打印
    li01 = reduce(lambda x, y: x + y, li01)  # 使用匿名函数
    print("对数组求和后打印" + str(li01))
    print("收工")
    return li01


# 第六题
# - 1. 读取zen.txt文件，并使用split()函数以空白为字符串分隔得到文件中所有的单词。
# - 2. 完成一个名为mimic_dict的函数：以出现在文件中的单词(全都小写化)为键(key)，
# 文件中所有紧跟在单词后面的一个单词组成的列表为值(value)。
def read_file_to_list(path: str) -> list[str]:
    """读取文件，分割单词，化为字典"""
    with open(path, 'r') as file:
        string = file.read()
    list1 = string.split()
    print("以空白为字符串分隔后：\n", list1)
    return list1


def mimic_dict(list0) -> dict[str, list]:
    """将list化为字典
    文件中的单词为key，单词后面的一个单词组成的列表为value。
    """
    list0 = list(map(lambda x: x.lower(), list0))  # 转化为小写
    list0 = list(map(lambda x: x.strip('*-.,'), list0))  # 去除其余的符号
    # print("处理后的链表：\n", list0)
    key = numpy.unique(list0)  # 去重复
    value = []
    for item1 in key:
        temp = []
        for index, item2 in enumerate(list0):
            if item1 == item2 and index + 1 < len(list0):
                temp.append(list0[index + 1])
        value.append(temp)
    dictionary: dict[str, list] = dict(zip(key, value))
    # print("dictionary:\n", dictionary)
    # print("key:\n", key)
    # print("value:\n", value)
    return dictionary
