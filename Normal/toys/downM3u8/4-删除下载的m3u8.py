# coding=utf-8
# @Time    : 2024/8/23 22:49
# @Software: PyCharm
import glob
import os


def delete_files(folder: str, extensions: list):
    """删除文件夹下指定后缀的文件"""
    for extension in extensions:
        for file_name in glob.glob(f'{folder}*.{extension}'):
            os.remove(file_name)


# 待删除ts、dat、m3u8的文件夹
ned_del_dir = "../../outputFile/downM3u8/"
# 开始删除
delete_files(ned_del_dir, ['ts', 'dat', 'm3u8'])
