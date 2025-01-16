# coding=utf-8
# @Time    : 2025-01-16 09:13:26
# @Software: PyCharm
import os


def delete_lines(filename: str) -> None:
    """
    删除 @MixJade Up 行之前的所有行,删除 @MixJade Down 之后的所有行

    :param filename: 文件路径
    """
    target1 = '@MixJade Up'  # 向上删除注解
    target2 = '@MixJade Down'  # 向下删除注解
    # 创建临时文件
    temp_filename = filename + '.bak'

    # 当需要保留的行找到时，把found设置为True
    found = False

    # 打开原始文件并创建一个新临时文件
    with open(filename, 'r', encoding='utf-8') as file, open(temp_filename, 'w', encoding='utf-8') as temp_file:
        for line in file:
            # 如果找到向下删除注解，则设置found为False
            if line.strip() == target2:
                found = False
            # 只有当found为True时才写入行
            if found:
                temp_file.write(line)
            # 如果找到向上删除注解，则设置found为True
            if line.strip() == target1:
                found = True

    # 替换原始文件
    os.remove(filename)
    os.rename(temp_filename, filename)


# 使用函数,
delete_lines(r"测试日志.txt")
