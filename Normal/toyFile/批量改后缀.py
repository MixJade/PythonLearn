# coding=utf-8
# @Time    : 2025/6/21 0:38
# @Software: PyCharm
import os


def change_extensions(folder_path, end_suffix):
    # 检查目录是否存在
    if not os.path.exists(folder_path):
        print(f"错误：目录 '{folder_path}' 不存在")
        return

    # 检查目录是否为文件
    if not os.path.isdir(folder_path):
        print(f"错误：'{folder_path}' 不是一个目录")
        return

    # 检查目录下是否存在子目录
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            print(f"错误：目录 '{folder_path}' 包含子目录 '{item}'，拒绝执行")
            return

    # 获取目录下的所有文件
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # 处理文件扩展名
    for filename in files:
        old_path = os.path.join(folder_path, filename)
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}.{end_suffix}"
        new_path = os.path.join(folder_path, new_filename)

        try:
            os.rename(old_path, new_path)
            print(f"已重命名: {old_path} -> {new_path}")
        except Exception as e:
            print(f"无法重命名 '{old_path}': {e}")


if __name__ == "__main__":
    # 手动输入目录路径
    fold_path = input("请输入要处理的目录路径: ").strip()
    # 处理路径中的波浪线 (~)
    fold_path = os.path.expanduser(fold_path)
    # 调用函数处理目录
    change_extensions(fold_path, "webp")
