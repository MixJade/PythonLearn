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


def process_folder(source_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for root, dirs, files in os.walk(source_folder):
        relative_path = os.path.relpath(root, source_folder)
        target_subfolder = os.path.join(target_folder, relative_path)
        if not os.path.exists(target_subfolder):
            os.makedirs(target_subfolder)
        for file in files:
            source_file_path = os.path.join(root, file)
            target_file_path = os.path.join(target_subfolder, file)
            create_symbolic_link(source_file_path, target_file_path)


if __name__ == "__main__":
    # 目标文件路径(必须是绝对路径)
    source_file = input("输入原文件(或文件夹)路径:").strip('"')
    if source_file == "":
        print("请输入文件路径")
        raise SystemExit(1)
    # 软链路径
    target_dir = input("输入目标文件夹路径(默认桌面):")
    if target_dir == "":
        target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    if os.path.isfile(source_file):
        file_name = os.path.basename(source_file)
        link = os.path.join(target_dir, file_name)
        create_symbolic_link(source_file, link)
    elif os.path.isdir(source_file):
        folder_name = os.path.basename(source_file)
        process_folder(source_file, os.path.join(target_dir, folder_name))
    else:
        print("输入的路径既不是文件也不是文件夹。")
