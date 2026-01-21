# coding=utf-8
# @Time    :2024-2-27 14:10:45
# @Software: PyCharm
import os


def merge_sql_files(dir_path: str, output_file_name: str) -> None:
    """将多个sql文件合并

    :param dir_path: 存放sql文件夹的路径
    :param output_file_name: 最终合成文件的输出路径
    """
    with open(output_file_name, 'w', encoding="utf8") as outfile:
        file_num = 0  # 文件数量
        empty_num = 0  # 连续空行数量
        for file_name in os.listdir(dir_path):
            if file_name == output_file_name:  # 跳过输出文件，否则会在合并时进入无限循环
                continue
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                file_num += 1
                if file_num > 1 and empty_num == 0:
                    # 每个文件开头加入空行(第一个文件除外)
                    outfile.write('\n')
                    empty_num += 1
                with open(file_path, 'r', encoding="utf8") as infile:
                    for line in infile:
                        if line != "\n" and line.strip() != ";":
                            empty_num = 0
                            outfile.write(line)
                    if empty_num == 0 and not line.endswith("\n"):
                        # 每个文件结尾加入空行(防止文件结尾不换行)
                        outfile.write('\n')
        print(f"最终融合 {file_num} 个文件，已输出至:{output_file_name}")


# 使用示例
merge_sql_files(r"sql文件集合", "合成的sql文件_结果.sql")
