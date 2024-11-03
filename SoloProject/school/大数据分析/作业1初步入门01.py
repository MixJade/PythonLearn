# coding=utf-8
# @Time    : 2022/11/22 22:00
# @Software: PyCharm
import unittest
from random import randint


class AttemptOne(unittest.TestCase):
    def test_how_many_stu(self):
        """一年级学生数量"""
        result = how_many_stu()
        self.assertEqual(302, result)

    def test_guess_number(self):
        """猜数字游戏"""
        guess_number(12, 5)  # 控制最大值和次数
        self.skipTest("猜数字游戏结束")


"""
1、某年级有若干名同学，
如果每9人一排会多出 5人，
如果每7个人一排会多出1人，
如果每5人一排会多出2人，
问这个年级至少有多少人？
"""


def how_many_stu() -> int:
    x: int = 0
    while True:
        x = x + 1
        if (x % 9 == 5) & (x % 7 == 1) & (x % 5 == 2):
            break
    print("这个班有 %d 人" % x)
    return x


"""
2、编写程序模拟猜数游戏。程序设定两个整数，一个数m表示要猜测的数的最大值，一个数n表示最多可以猜测的次数，m和n的值可以根据需要调整。
（1）系统运行时首先生成一个1~m之间随机整数；
（2）然后提示用户进行猜测并根据用户输入进行必要的提示（猜对了、猜大了、猜小了）；
（3）如果猜对则提前结束程序；如果猜错，提示用户继续；如果次数用完仍没有猜对，提示游戏结束并给出正确答案。
"""


def guess_number(max_num: int, max_time: int) -> None:
    """猜数字游戏

    :param max_num: 最大数字
    :param max_time: 猜的次数
    """
    print("开始踹数字游戏,最大值是 %d,最多踹 %d 次" % (max_num, max_time))
    value = randint(1, max_num)  # 随机生成一个整数
    for i in range(max_time):
        prompt = '请输入您猜的数字:' if i == 0 else '请再猜一次:'
        try:
            x = int(input(prompt))  # 防止不是整数
        except ValueError:
            print('必须输入整形数，且在数字1和 %d 之间' % max_num)
        else:
            if x == value:
                print('猜对了!!!!! ')
                break
            elif x > value:
                print('猜大了！')
            else:
                print('猜小了！')
    else:
        print('游戏结束，您失败了！\n 答案是:', value)
