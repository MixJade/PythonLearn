# coding=utf-8
# @Time    : 2024/2/22 17:45
# @Software: PyCharm
import os


def walk_dir(dir_path: str) -> None:
    """遍历文件夹下的所有子文件夹

    :param dir_path: 父文件夹路径
    """
    print(dir_path)
    up_md_title(dir_path)
    for root, dirs, files in os.walk(dir_path):
        for son_dir in dirs:
            walk_dir(os.path.join(root, son_dir))


def up_md_title(directory: str) -> None:
    """遍历文件夹下的md文件，并将文件名作为md的标题
    只遍历当前文件夹下的文件，不会打开其内部的文件夹

    :param directory: 存有md的文件夹的路径
    """
    # 遍历文件夹下的md文件
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            file_path: str = os.path.join(directory, filename)

            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as file:
                lines: list[str] = file.readlines()

            # 对于已经有标题的，要删除标题
            if lines[0].startswith("# "):
                lines.pop(0)
            # 删除文件的前面的空行
            end: int = next((i for i, x in enumerate(lines) if x != '\n'), None)
            del lines[0:end]
            # 将文件名变成新的标题
            lines.insert(0, f"# {filename.replace('.md', '')}\n\n")

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as file:
                print("-->" + filename)
                file.writelines(lines)


# 待规范标题的、存有md的文件夹
walk_dir(r"testData")
