# coding=utf-8
# @Time    : 2021/11/9 16:30
# @Software: PyCharm
import unittest
from collections import Counter


class AttemptThree(unittest.TestCase):
    """入门案例3:面向对象和综合训练。"""

    def test_question_1(self):
        """顺风划船"""
        expected = 3
        result = direction_pred((2, 3), (3, 5), ['N', 'S', 'W', 'E', 'N'])
        print("到达目的地需要的时间为：", result)
        self.assertEqual(expected, result)

    def test_question_2(self):
        """类的使用"""
        car = Car("A", "M")
        car.show()
        car.run()
        self.skipTest("看类的输出")

    def test_question_3(self):
        """继承类的使用"""
        car = Car2("A", "M", 10)
        car.show()
        car.run()
        car.set_people(5)
        car.reduce_people()
        car.increase_people()
        self.skipTest("看继承类的输出")

    def test_question_4(self):
        """蛇形填数"""
        expected = 761
        result = snake_fill_number(20, 20)
        print("蛇形填数的第20行20列的数为:", result)
        self.assertEqual(expected, result)


# 第一题
# 顺风快递的原理就是利用每个时刻的风向来运送货物，这样可以做到节能减排。现在已知
# 起点给和终点的坐标，以及接下来 n 个时刻的风向(东南西北)，每次可以选择顺风偏移1个
# 单位或者停在原地。求到达终点的最少时间。
# 输入格式：
# 第一行两个正整数 x1,y1，表示小明所在位置。
# 第二行两个正整数 x2,y2，表示小明想去的位置。
# 第三行，表示风向，即东南西北的英文单词的首字母。
def direction_pred(p1: tuple[int, int], p2: tuple[int, int], direction: list[str]) -> int:
    """顺风划船
    每次可以选择顺风偏移或者停在原地。求到达终点的最少时间。

    :param p1: 小明所在位置的坐标
    :param p2: 小明想去的坐标
    :param direction: 接下来n个时刻的风向
    :return: 到达目的地需要的时间
    """
    # 判断方位
    dx = int(p2[0]) - int(p1[0])
    dy = int(p2[1]) - int(p1[1])
    # 计算各方向的数量
    # 这里有bug，如果输入的风向不够4种，会因为键值缺少而报错
    a2 = dict(Counter(direction))
    print("各方向风向的数量：", a2)
    # 设置需要的时间，-1表示无法到达目的地
    need_time = -1
    if dx == 0:
        if dy > 0:  # N
            if a2['N'] >= dy:
                need_time = dy
        else:  # S
            if a2['S'] >= abs(dy):
                need_time = abs(dy)
    elif dx > 0:
        if dy == 0:  # E
            if a2['E'] >= dx:
                need_time = dx
        elif dy > 0:  # E N
            if a2['E'] >= dx and a2['N'] >= dy:
                need_time = dx + dy
        else:
            if a2['E'] >= dx and a2['N'] >= abs(dy):
                need_time = dx + abs(dy)
    else:
        if dy == 0:  # W
            if a2['W'] >= abs(dx):
                need_time = abs(dx)
        elif dy > 0:  # W N
            if a2['W'] >= abs(dx) and a2['N'] >= dy:
                need_time = abs(dx) + dy
        else:  # W S
            if a2['W'] >= abs(dx) and a2['S'] >= abs(dy):
                need_time = abs(dx) + abs(dy)
    return need_time


# 第二题
# 创建一个名为 Car 的类，其方法__init__() 设置两个属性:name 和 brand(品牌)。
# 定义一个名为 show()的方法，功能是打印出汽车的名称和品牌。
# 定义一个名为 run()的方法，打印:汽车 XX 跑起来了。其中 XX 表示汽车的 name.
# 根据这个类创建一个名为 car 的实例，调用上面的两个方法打印其两个属性。
class Car:
    def __init__(self, name, brand):
        self.name = name
        self.brand = brand

    def show(self):
        print(f"汽车的名称是 {self.name}， 品牌为 {self.brand}")

    def run(self):
        print(f"汽车{self.name}跑起来了")


# 第三题
# 在（2）的 Car 类中，添加number_of_people属性，并将其默认值设置为 0。
# 添加max_people的属性，表示车上最多可以有几个人。修改相应的构造方法，传入max_people的值。
# 添加set_people()方法，设置车上的人数，但不超过max_people的限制。
# 添加increase_people()方法，每次调用会让车上的人数加1，但不超过max_people的限制。
# 添加reduce_people()方法，每次调用会让车上的人数减少1，但最多减少为0.
# 根据这个类创建一个名为 car 的实例，调用（2）的两个方法打印其两个属性。
# 打印有多少人在车上，然后多次调用以上3个方法，并打印车上的人数。
class Car2(Car):
    def __init__(self, name, brand, max_people):
        super().__init__(name, brand)  # 调用父类构造函数
        self.brand = brand
        self.number_of_people = 0
        self.max_people = max_people

    def set_people(self, num):
        if num < self.max_people:
            self.number_of_people = num
        else:
            self.number_of_people = self.max_people
            print(f'现有{self.number_of_people}在车上')

    def increase_people(self):
        if self.number_of_people < self.max_people:
            self.number_of_people += 1
            print(f'新增1人，现有{self.number_of_people}人在车上')
        else:
            print(self.max_people), print('满了')

    def reduce_people(self):
        if self.number_of_people > 0:
            self.number_of_people -= 1
            print(f'减少1人，现有{self.number_of_people}人在车上')
        else:
            print(f'车上没人')


# 第四题 蛇形填数
# 比如输入3，最终输出一个3x3的矩阵，
# 矩阵样式如下：
# 1 2 6...
# 3 5...
# 4...
# 请编程计算a行b列的数是多少？
# 测试数据a=20，b=20
def snake_fill_number(line_num: int, column_num: int) -> int:
    """蛇形填数
    :param line_num: 行号
    :param column_num: 列号
    :return: 指定行列的数
    """
    c = line_num + column_num - 1  # 第几斜排
    n = 0
    for i in range(1, c + 1):
        n += i  # c 斜排的最后一个数
    if c % 2 != 0:  # 奇偶性
        ans = n - line_num + 1  # 等于最大的数减行数加 1
    else:
        ans = n - column_num + 1  # 等于最大的数减列数加 1
    return ans
