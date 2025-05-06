# coding=utf-8
# @Time    : 2025/4/18 14:57
# @Software: PyCharm
import os


def create_hard_link(source_file: str, destination_file: str) -> None:
    try:
        # 创建硬链接
        os.link(source_file, destination_file)
        print(f"硬链接已成功创建，从 {source_file} 到 {destination_file}")
    except FileExistsError:
        print(f"错误: 目标文件 {destination_file} 已存在。")
    except FileNotFoundError:
        print(f"错误: 源文件 {source_file} 未找到。")
    except PermissionError:
        print("错误: 没有足够的权限创建硬链接。")
    except Exception as e:
        print(f"发生未知错误: {e}")


# 示例用法
source_file_path = r"../main.py"
destination_file_path = '../outputFile/硬链接.py'
create_hard_link(source_file_path, destination_file_path)
