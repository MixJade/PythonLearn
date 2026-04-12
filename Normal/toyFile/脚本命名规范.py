# coding=utf-8
# @Time    : 2026/4/12 15:52
# @Software: PyCharm
import os

"""
给py脚本规范命名
"""


def get_py_files(folder_path):
    # 存储所有py文件名
    py_files = []

    # 检查路径是否存在
    if not os.path.isdir(folder_path):
        print("错误：输入的文件夹路径不存在！")
        return py_files

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        # 判断是否为 .py 文件（忽略大小写）
        if file_name.lower().endswith('.py'):
            py_files.append(file_name)

    return py_files


if __name__ == "__main__":
    # 获取用户输入的文件夹路径
    folder = input("请输入文件夹路径：").strip()

    # 获取所有py文件
    result = get_py_files(folder)

    # 输出结果
    if result:
        print(f"\n该文件夹下共有 {len(result)} 个 .py 文件：\n")
        for name in result:
            print(f"为”{name}“起一个大驼峰的名字")
    else:
        print("\n该文件夹下没有找到 .py 文件")
