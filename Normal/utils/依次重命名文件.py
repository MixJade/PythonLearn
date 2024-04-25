# coding=utf-8
# @Time    : 2024/3/27 23:30
# @Software: PyCharm
import os


def rename_file(file_path: str, new_name: str) -> None:
    """重命名文件

    :param file_path: 文件路径,如"your/file/o_nm.jpg"
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


def input_file_name():
    """循环输入要重命名的文件路径
    """
    base_name = input("请输入基础名字：")
    i = input("请输入起始序列(默认1)：")
    if i.isdigit():
        i = int(i)
    else:
        i = 1
    while True:
        random_string = input("请输入文件路径(输0退出)：")
        if random_string.lower() == '0' or random_string.lower() == '':
            break
        rename_file(random_string, f"{base_name}{i:03d}")
        i += 1


if __name__ == "__main__":
    input_file_name()
