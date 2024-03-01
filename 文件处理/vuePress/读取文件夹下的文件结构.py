# coding=utf-8
# @Time    : 2024/3/1 17:07
# @Software: PyCharm
import os


def list_files(dir_path: str) -> dict[str, str | list]:
    """读取文件下的目录结构，并输出成vuePress的配置文件形式

    :param dir_path: 目标文件夹
    """
    result = {'text': os.path.basename(dir_path), 'collapsible': 'true', 'children': []}

    # 遍历目录下的所有子目录和文件
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)

        # 如果是文件，则直接添加文件名
        if os.path.isfile(item_path):
            children_str: str = item_path.replace(target_dir, "").replace("\\", "/")
            result['children'].append(children_str)
        # 如果是目录，则递归调用该函数
        else:
            result['children'].append(list_files(item_path))

    return result


# 目标文件夹
target_dir = r"E:\MyCode\TsLearn\my-page\docs"
# javaLearn的文件夹输出结构
files_list = list_files(target_dir + r"\javaLearn")
print(r'"/javaLearn/":', end=' ')
print(files_list['children'], end=',\n')
# tsLearn的文件夹输出结构
files_list = list_files(target_dir + r"\tsLearn")
print(r'"/tsLearn/":', end=' ')
print(files_list['children'], end=',\n')
# pyLearn的文件夹输出结构
files_list = list_files(target_dir + r"\pyLearn")
print(r'"/pyLearn/":', end=' ')
print(files_list['children'], end=',\n')
