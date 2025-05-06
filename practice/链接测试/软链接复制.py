# coding=utf-8
# @Time    : 2025/4/18 14:57
# @Software: PyCharm
import os


def create_symbolic_link(target_path, link_path):
    try:
        # 创建软链接
        os.symlink(target_path, link_path)
        print(f"成功创建软链接: {link_path} 指向 {target_path}")
    except FileExistsError:
        print(f"错误: 软链接 {link_path} 已经存在。")
    except PermissionError:
        print(f"错误: 没有足够的权限创建软链接 {link_path}。")
    except OSError as e:
        print(f"错误: 创建软链接时发生系统错误: {e}")


if __name__ == "__main__":
    # 目标文件或目录的路径(必须是绝对路径)
    # target = r"E:\MyCode\PythonLearn\practice\main.py"
    target = os.path.join(os.path.dirname(os.getcwd()), "main.py")
    print(target)
    # 软链接的路径
    link = '../outputFile/软链接.py'
    create_symbolic_link(target, link)
