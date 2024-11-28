# coding=utf-8
# @Time    : 2022/11/22 22:00
# @Software: PyCharm
"""
3、模拟一个简单的成绩输入程序。要求如下。
（1）学生信息至少包含：学号、姓名、性别、成绩；
（2）以自己和其他至少2个同学真实信息进行输入，成绩自定。
（3）把所有信息保存到文件，文件名：student.txt 。
（4）然后读出student.txt中的信息。
"""
from dataclasses import dataclass


@dataclass
class Student:
    """封装学生类"""
    ID: str = ''
    name: str = ''
    sex: str = ''
    grade: int = 0


def add(stu_list01, stu):
    """
    添加一个学生

    :param stu_list01: 学生列表
    :param stu: 单个学生
    """
    stu_list01.append(stu)
    file_object = open(file, "a", encoding='utf-8')
    file_object.write(stu.ID)
    file_object.write(" ")
    file_object.write(stu.name)
    file_object.write(" ")
    file_object.write(stu.sex)
    file_object.write(" ")
    file_object.write(str(stu.grade))
    file_object.write("\n")
    file_object.close()
    print("保存成功！")


def display(stu_list02):  # 显示所有学生信息
    for item in stu_list02:
        print("学号:%s 姓名:%s 性别:%s 成绩:%s" % (item.ID, item.name, item.sex, item.grade))


def init(stu_list03):
    """
    初始化函数
    """
    file_object = open(file, 'w+', encoding='utf-8')
    for line in file_object:
        stu = Student()
        line = line.strip("\n")
        s = line.split(" ")
        stu.ID = s[0]
        stu.name = s[1]
        stu.sex = s[2]
        stu.grade = s[3]
        stu_list03.append(stu)
    file_object.close()
    print("初始化成功！")
    main()


def main():
    while True:
        print("输入1开始插入，输入2展示所有学生,输入0终止")
        choose = input("请输入你的选择：")
        if choose == "1":
            stu = Student()
            stu.ID = input("请输入学生的学号")
            stu.name = input("请输入学生的姓名")
            stu.sex = input("请输入学生的性别")
            stu.grade = input("请输入学生的成绩")
            add(stu_list, stu)

        if choose == '2':
            display(stu_list)

        if choose == '0':
            break


if __name__ == '__main__':
    file = '../A2兼收并蓄/students.txt'
    stu_list = []
    init(stu_list)
