# coding=utf-8
# @Time    : 2024/2/5 16:37
# @Software: PyCharm
import os
import shutil


def remove_dirs(start_path: str, dir_name: str) -> None:
    """删除某一文件夹下的文件夹

    :param start_path: 父文件夹
    :param dir_name: 待删除的子文件夹
    """
    dir_sum = 0
    for dir_path, dir_names, filenames in os.walk(start_path):
        if dir_name in dir_names:
            shutil.rmtree(os.path.join(dir_path, dir_name))
            dir_sum += 1
    print(f"目录{start_path}下的{dir_sum}个{dir_name}文件夹已清除")


# 清除Java项目下所有的.idea目录与target目录
java_dir_path = r"C:\MyCode\JavaLearn"
remove_dirs(java_dir_path, '.idea')
remove_dirs(java_dir_path, 'target')
remove_dirs(java_dir_path, '.mvn')
