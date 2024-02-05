def file_attempt():
    """读取文件的名字、状态，属性，编码"""
    file = open('列表与继承.py', encoding='utf-8')
    print(file)
    print(file.name)
    print(file.closed)
    print(file.mode)
    print(file.encoding)
    file.close()


def read_attempt():
    """read函数用于读取文本里面的内容"""
    file = open('列表与继承.py', encoding='utf-8')
    text = file.read()
    print(text)
    file.close()


def read_line_attempt():
    """把获取到的内容按行读取需用readLine函数"""
    file = open('列表与继承.py', encoding='utf-8')
    print("readline函数")
    print(file.readline())
    print(file.readline(4))
    file.close()


if __name__ == '__main__':
    file_attempt()
    read_attempt()
    read_line_attempt()
