dict1 = {'id': '1234', 'name': '张三', 'age=': 18}
dict2 = {'id': '1235', 'name': '张四', 'age=': 18}
dict3 = {'id': '1236', 'name': '张五', 'age=': 18}
dict4 = {'id': '1237', 'name': '张六', 'age=': 18}

list1 = [dict1, dict2, dict3, dict4]
print(list1)

a = 'abcdefgh'
print(a[0::2])
print(a.split('b'))
print(a.replace('c', 'a'))
print(a.count('e'))
print(a.index('f'))
print("这个字符串是%s" % a)
print("这个字符串是{0},{0}".format(a))
print(f"这个字符串是{a}")


class A:
    def f_1(self):
        print("父代一号")


class B:
    def f_2(self):
        print("父代二号")


class C(A, B):
    def __init__(self):
        print("子代一号")

    def f_3(self):
        self.f_1()
        self.f_2()


c = C()
c.f_3()

count = 0
for i in range(100):
    a = input("请输入对男主要说的话:")
    if a == "hi":
        print("开启时间重启!")
        print("次数", str(count + 1))
        count += 1
        print("============")
    else:
        print("============")
