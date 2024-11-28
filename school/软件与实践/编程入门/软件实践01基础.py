# coding=utf-8
# @Time    : 2021/11/2 16:30
# @Software: PyCharm
import unittest


class AttemptOne(unittest.TestCase):
    """入门案例01:
    掌握Python流程控制语句，与unittest的基本使用
    (单元测试一般另起文件，但这里单纯的学习，不必多此一举)
    """

    def test_question_1(self):
        """计算1!+2!+3!+...+9!的值"""
        result = factorial_1_9()
        self.assertEqual(46233, result)

    def test_question_2(self):
        """辗转相除法求最大公约数"""
        result = greatest_common_divisor(24, 36)
        self.assertEqual(12, result)

    def test_question_3(self):
        """统计字符串中字母、空格、数字、字符的个数"""
        expected = (5, 2, 3, 3)
        result = statistics_str("lbw nb !!!111")
        self.assertEqual(expected, result)

    def test_question_4(self):
        """统计Sn值，Sn=a+aa+aaa+...+aa...a(n个a)"""
        result = sum_sn(9, 6)
        self.assertEqual(result, 740740734)

    def test_question_5(self):
        """输出所有的水仙花数"""
        expected = [153, 370, 371, 407]
        result = narcissistic_number()
        self.assertEqual(expected, result)

    def test_question_6(self):
        """找出1000以内的所有完数"""
        expected = [6, 24, 28, 496]
        result = perfect_number()
        self.assertEqual(expected, result)

    def test_question_7(self):
        """求分数序列 2/1,3/2,5/3...前20项之和"""
        expected = 32.66026079864164
        result = sum_20_fraction()
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()


def factorial_1_9() -> int:
    """计算1!+2!+3!+...+9!的值

    :return: 阶乘相加结果
    """
    circle_sum: int = 0
    for circle_i in range(1, 9):
        circle_tem = 1
        for j in range(1, circle_i + 1):
            circle_tem = circle_tem * j
        circle_sum = circle_sum + circle_tem
    print("结果是：", circle_sum)
    return circle_sum


def greatest_common_divisor(m: int, n: int) -> int:
    """辗转相除法求最大公约数
    """
    if m < n:
        m, n = n, m
    while 1:
        r = m % n
        if r == 0:
            print("最大公约数是：", n)
            return n
        else:
            m, n = n, r


def statistics_str(str001: str) -> tuple[int, int, int, int]:
    """统计字符串中字母、空格、数字、字符的个数
    """
    letters, space, number, other = 0, 0, 0, 0
    for i in range(0, len(str001)):
        if 'a' <= str001[i] <= 'z':
            letters += 1
        elif str001[i] == ' ':
            space += 1
        elif '0' <= str001[i] <= '9':
            number += 1
        else:
            other += 1
    print("字母 = %d, 空格 = %d, 数字 = %d, 其他字符 = %d" % (letters, space, number, other))
    return letters, space, number, other


def sum_sn(n: int, a: int) -> int:
    """统计Sn值，Sn=a+aa+aaa+...+aa...a(n个a)

    :param n: a的位数
    :param a: 1位数字
    :return: Sn的值
    """
    sn = 0
    for i in range(1, n + 1):
        tem = 0
        for j in range(0, i):
            tem += a * 10 ** j
        sn += tem
    print("Sn =", sn)
    return sn


# 第五题
def narcissistic_number() -> list[int]:
    """输出所有的水仙花数(各位数字的立方和等于其本身)
    """
    narcissistic_number_list = []
    for i in range(100, 1000):
        if (int(i // 100)) ** 3 + (int((i % 100) // 10)) ** 3 + (i % 10) ** 3 == i:
            print(i)
            narcissistic_number_list.append(i)
    return narcissistic_number_list


def perfect_number() -> list[int]:
    """找出1000以内的所有完数
    (其本身以外的因子之和等于本身，如6=1+2+3)
    """
    perfect_number_list = []
    for i in range(6, 1001):
        str001 = ''
        sum02 = 0
        for j in range(1, i):
            if i % j == 0:
                sum02 += j
                str001 += '%d ' % j
                if sum02 == i:
                    perfect_number_list.append(i)
                    print("%d 的完数公式" % i, end=' ')
                    print(str001)
    return perfect_number_list


def sum_20_fraction() -> float:
    """有一个分数序列 2/1,3/2,5/3...
    求这个序列的前20项之和
    """
    sum01 = 0
    a = 2
    b = 1
    for n in range(0, 20):
        print(f"{a}/{b}={a / b}")
        sum01 += a / b
        c = a
        a = a + b
        b = c
    print("前20项之和为：", sum01)
    return sum01
