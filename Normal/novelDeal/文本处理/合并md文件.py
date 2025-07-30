# coding=utf-8
# @Time    : 2024/8/17 20:26
# @Software: PyCharm
import os


def merge_md_files(dir_path: str) -> None:
    """将多个md文件合并

    :param dir_path: 存放sql文件夹的路径
    """
    output_file_name = "融合的文件.md"  # 输出文件名称
    output_file_path = os.path.join(dir_path, output_file_name)  # 输出文件路径
    # 开始合并
    with open(output_file_path, 'w', encoding="utf8") as outfile:
        file_num = 0
        outfile.write(f"# {output_file_name}\n")
        for file_name in os.listdir(dir_path):
            if file_name == output_file_name:  # 跳过输出文件，否则会在合并时进入无限循环
                continue
            if not file_name.endswith(".md"):  # 不是md文件就跳过
                continue
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                outfile.write("\n")
                file_num += 1
                with open(file_path, 'r', encoding="utf8") as infile:
                    for line in infile:
                        if line.startswith('# ') or line.startswith('## ') or line.startswith('### '):
                            line = '#' + line
                        outfile.write(line)
        print(f"最终融合 {file_num} 个文件，已输出至:{output_file_name}")


# 使用示例(输入文件夹)
merge_md_files(r"testData")
