# coding=utf-8
# @Time    : 2025/5/16 16:02
# @Software: PyCharm
import os


def create_symbolic_link(target_path, link_path):
    try:
        os.symlink(target_path, link_path)
        print(f"创建软链: {link_path} 指向 {target_path}")
    except FileExistsError:
        print(f"错误: 文件 {link_path} 已经存在。")
    except PermissionError:
        print(f"错误: 没有足够的权限创建软链 {link_path}。")
    except OSError as e:
        print(f"错误: 创建软链时发生系统错误: {e}")


if __name__ == "__main__":
    # 目标文件路径(必须是绝对路径)
    source_file = input("输入原文件路径:").strip('"')
    if source_file == "":
        print("请输入文件路径")
        raise SystemExit(1)
    # 软链路径
    target_dir = input("输入目标文件夹路径(默认桌面):")
    file_name = os.path.basename(source_file)
    if target_dir == "":
        target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    link = os.path.join(target_dir, file_name)
    create_symbolic_link(source_file, link)
