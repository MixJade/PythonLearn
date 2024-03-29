# coding=utf-8
# @Time    : 2024/3/1 17:07
# @Software: PyCharm
import os
import shutil


def copy_files(src_dir: str, dst_dir: str) -> None:
    """将一个文件夹的文件，复制到另一个文件夹中

    :param src_dir: 源文件夹
    :param dst_dir: 目标文件夹，不存在会自动新建
    """
    print("目标文件夹:", dst_dir)
    if not os.path.exists(dst_dir):
        # 如果目标文件夹不存在则自动新建
        os.makedirs(dst_dir)

    for filename in os.listdir(src_dir):
        src_file: str = os.path.join(src_dir, filename)
        dst_file: str = os.path.join(dst_dir, filename)
        # 遍历目录下的所有子目录和文件
        if os.path.isfile(src_file):
            # `shutil.copy2`还复制文件的元数据(如修改时间和权限位)
            shutil.copy2(src_file, dst_file)
        else:
            copy_files(src_file, dst_file)


# 存放代码的公共文件夹
# (当前文件的上三级目录)等价于r"C:\MyCode"
code_dir = os.path.abspath(os.path.join(os.getcwd(), "../../../.."))
# 目标文件夹
target_dir = code_dir + r"\TsLearn\my-page\docs"
# 复制Java笔记
copy_files(code_dir + r'\JavaLearn\docs\2023', target_dir + r"\javaLearn")
# 复制Python笔记
copy_files(code_dir + r'\PythonLearn\docs', target_dir + r"\pyLearn")
# 复制前端笔记
copy_files(code_dir + r'\TsLearn\docs', target_dir + r"\tsLearn")
