# coding=utf-8
# @Time    : 2022/10/25 21:00
# @Software: PyCharm
import unittest

filename = "../A2兼收并蓄/文件读写测试.txt"


class AttemptFile(unittest.TestCase):
    def test_write_file(self):
        """文件写入"""
        file_text = '''老冯啊，
杀两只鸡，炖锅鸡汤
我说杀鸡的事，你听到没有
'''
        f = open(filename, 'w', encoding='utf-8')
        f.write(file_text)
        f.close()
        self.skipTest("文件写入")

    def test_read_file(self):
        """文件读取"""
        f = open(filename, 'r', encoding='utf-8')
        read_str = f.read()
        print(read_str)
        f.close()
        self.skipTest("文件读取")

    def test_write_apple_file(self):
        """文件写入追加(参数a)"""
        file_text = "\n听到了，听到了啊"
        f = open(filename, 'a', encoding='utf-8')
        f.write(file_text)
        f.close()
        self.skipTest("文件写入追加")

    def test_write_replace_file(self):
        """文件写入替换(参数r+)"""
        f = open(filename, 'r+', encoding='utf-8')
        f.write("\n穿山甲!")
        print(f.read())  # 刚写入的不会被读取出来
        f.close()
        self.skipTest("文件写入替换(参数r+)")

    def test_read_in_exception(self):
        """在try-catch中读取文件"""
        try:
            f = open(filename, 'r', encoding='utf-8')
            print(f.read())
        except UnicodeDecodeError:
            print("读取失败，字符编码异常")
        else:
            print("打开成功")
        finally:
            print("还是熟悉的finally")
        self.skipTest("在try-catch中读取文件")

    def test_with_auto_close(self):
        """用with语句，自动关闭
        这里第一行是空行，且end是没有自动换行的
        而且换行符是在每一行末尾
        所以成这个效果，其实end是加在末尾的
        """
        with open(filename, encoding='utf-8') as f:
            for line in f:
                print(line, end="啊")
        # 上面的end=“啊”覆盖了Py默认的换行符，所以最后一个“啊”会在END前面
        print("=====END=====")
        self.skipTest("用with语句，自动关闭")


if __name__ == '__main__':
    unittest.main()
