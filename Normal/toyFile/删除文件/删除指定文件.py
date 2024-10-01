# coding=utf-8
# @Time    : 2024/3/8 11:00
# @Software: PyCharm
import os


def delete_specific_files(directory: str, file_name_list: list[str]):
    """从一个文件夹中，删除特定的文件

    :param directory: 文件夹的绝对路径
    :param file_name_list: 待删除的文件名称(多个)
    """
    for folder_name, _, filenames in os.walk(directory):  # 使用os.walk进行遍历
        for filename in filenames:
            if filename in file_name_list:  # 如果在遍历过程中找到了指定的文件名
                file_path = os.path.join(folder_name, filename)  # 通过os.path.join连接目录和文件名，得到完整的文件路径
                os.remove(file_path)  # 使用os.remove删除文件
                print(f"Deleted file : {file_path}")  # 输出删除文件的信息


# 需要删除的文件
need_del_file = ['有标题但不匹配的md.md',
                 'TABLE_ONE.sql',
                 ]
# 调用函数，删除目录及其子目录下的指定文件
delete_specific_files(r'../inputFile', need_del_file)
