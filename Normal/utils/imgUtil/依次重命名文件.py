# coding=utf-8
# @Time    : 2024/3/27 23:30
# @Software: PyCharm
import os
import re


def rename_file(file_path: str, new_name: str) -> None:
    """重命名文件

    :param file_path: 目标文件路径
    :param new_name: 新的文件名,如"new_name"
    """
    # 分割文件名和后缀
    file_name, file_extension = os.path.splitext(file_path)
    # 获取文件路径
    directory = os.path.dirname(file_path)
    # 将新名称和旧的扩展名拼接成新的文件路径
    new_file_path = os.path.join(directory, new_name + file_extension)
    # 重命名文件
    os.rename(file_path, new_file_path)
    print(f"已重命名为{new_name}")


def try_int(s: str) -> int | str:
    try:
        return int(s)
    except ValueError:
        return s.lower()


def alphanum_key(s: str) -> list[int]:
    return [try_int(c) for c in re.split('([0-9]+)', s)]


def rename_all_file(file_path: str, begin_num: int) -> None:
    """批量重命名文件夹下所有文件

    :param file_path: 目标文件夹下的某个文件
    :param begin_num: 起始序列
    """
    # 获取文件路径
    directory = os.path.dirname(file_path)
    # 获取文件夹中所有的文件（只读取文件，不读取文件夹）
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    # 解析字符串中的数字、不区分字母大小写排序
    files.sort(key=alphanum_key)
    for file in files:
        # 按文件名顺序重命名
        rename_file(os.path.join(directory, file), f"{base_name}{begin_num:03d}")
        begin_num += 1


if __name__ == "__main__":
    # 循环输入要重命名的文件路径
    base_name = input("请输入基础名字：")
    i = input("请输入起始序列(默认1)：")
    if i.isdigit():
        i = int(i)
    else:
        i = 1
    # 选择方案
    print("方案1:依次重命名文件,方案2:重命名文件夹下所有文件")
    plan_str = input("请选择你的方案:")
    # 方案2:重命名文件夹下所有文件
    if plan_str == '2':
        file_string = input("输入目标文件夹下某个文件路径：")
        rename_all_file(file_string.strip('"'), i)
    # 方案1:依次重命名文件
    else:
        while True:
            random_string = input("请输入文件路径(输0退出)：")
            if random_string == '0' or random_string == '':
                break
            rename_file(random_string.strip('"'), f"{base_name}{i:03d}")
            i += 1
