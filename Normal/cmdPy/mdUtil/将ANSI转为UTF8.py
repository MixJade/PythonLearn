# coding=utf-8
# @Time    : 2024/3/7 20:07
# @Software: PyCharm
import chardet


def see_file_chardet():
    """检查文件的编码
    """
    r_file = open(file_name, 'rb').read()
    result = chardet.detect(r_file)
    return result['encoding']


def tran_ansi_to_utf8():
    """将ansi格式的文件转为utf8
    """
    # 打开原始文件，以 ANSI 编码
    # mbcs是微软用来表示默认编码的。
    with open(file_name, 'r', encoding='mbcs') as file:
        contents = file.read()

    # 写入新文件，以 UTF-8 编码
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(contents)
    print("该文件成功转为utf-8格式")


def tran_utf8_to_ansi():
    """将utf8格式的文件转为ansi
    """
    with open(file_name, 'r', encoding='utf-8') as file:
        contents2 = file.read()
    with open(file_name, 'w', encoding='mbcs') as file:
        file.write(contents2)
    print("该文件成功转为ANSI格式")


if __name__ == '__main__':
    file_name = input("请输入ANSI文件路径(可直接拖入终端):").strip('"')
    file_chardet = see_file_chardet()
    print("文件编码为", file_chardet)
    if file_chardet == 'utf-8':
        choose = input("该文件可能已是UTF8格式,是否转为ANSI格式?(1是0否)")
        if choose == '1':
            tran_utf8_to_ansi()
    elif file_chardet == 'GB2312':
        tran_ansi_to_utf8()
    else:
        print("未知编码")
