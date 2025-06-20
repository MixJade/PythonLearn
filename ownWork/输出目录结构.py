# coding=utf-8
# @Time    : 2025/6/20 15:11
# @Software: PyCharm
import os


def generate_tree(path, prefix=''):
    """生成目录树结构"""
    # 获取所有文件和文件夹
    items = os.listdir(path)
    # 排序，文件夹在前，文件在后
    items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x))

    for i, item in enumerate(items):
        # 排查部分目录
        if item == ".idea":
            continue
        # 正常执行
        item_path = os.path.join(path, item)
        is_dir = os.path.isdir(item_path)

        # 判断是否是最后一个项目
        is_last = i == len(items) - 1
        # 设置当前行的前缀
        line_prefix = '└── ' if is_last else '├── '
        # 设置下一行的前缀
        next_prefix = prefix + ('    ' if is_last else '│   ')

        # 打印当前项目
        print(f"{prefix}{line_prefix}{item}/" if is_dir else f"{prefix}{line_prefix}{item}")

        # 递归处理子目录
        if is_dir:
            generate_tree(item_path, next_prefix)


if __name__ == "__main__":
    # 获取当前脚本所在目录
    current_dir = os.getcwd()
    print(f"目录结构 - {current_dir}")
    print("=" * 50)
    generate_tree(current_dir)
