# coding=utf-8
# @Time    : 2024/3/7 20:07
# @Software: PyCharm

# file_name = 'inputFile/待删除数据.csv'
file_name = input("请输入ANSI文件路径(可直接拖入终端):")

try:
    # 打开原始文件，以 ANSI 编码
    # mbcs是微软用来表示默认编码的。
    with open(file_name, 'r', encoding='mbcs') as file:
        contents = file.read()

    # 写入新文件，以 UTF-8 编码
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(contents)
    print("该文件成功转为utf-8格式")
except UnicodeDecodeError:
    print("该文件不是ANSI格式")
