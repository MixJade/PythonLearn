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
        file_num = 0
        for file_name in os.listdir(dir_path):
            if file_name == output_file_name:  # 跳过输出文件，否则会在合并时进入无限循环
                continue
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                file_num += 1
                with open(file_path, 'r', encoding="utf8") as infile:
                    for line in infile:
                        if line.startswith('create table'):
                            outfile.write(get_table_name(line))
                        outfile.write(line)
        print(f"最终融合 {file_num} 个文件，已输出至:{output_file_name}")


def get_table_name(query: str) -> str:
    """通过建表语句获取表名并加注释

    :param query: 建表语句,形如"create table TABLE_TWO"
    :return: 建表的分割注释
    """
    words = query.split(" ")
    if len(words) > 2 and (words[0] + " " + words[1] == "create table"):
        line_str: str = '-- ----------------------------\n'
        return f"\n{line_str}-- Table structure for {words[2]}{line_str}"
    else:
        return query


# 使用示例
merge_sql_files("../../inputFile/SQL文件/合并sql文件", "../../outputFile/合成的sql文件.sql")
