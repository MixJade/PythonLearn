# coding=utf-8
# @Time    : 2024/3/1 17:07
# @Software: PyCharm
import json
import os
from pprint import pprint


def list_files(dir_path: str) -> dict[str, bool | list | str]:
    """读取文件下的目录结构，并输出成vuePress的配置文件形式

    :param dir_path: 目标文件夹
    """
    result = {"text": os.path.basename(dir_path), "collapsible": True, "children": []}

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


def get_first_child(data: dict[str, bool | list | str] | str) -> str:
    """查询嵌套目录结构的第一个路径
    """
    if 'children' in data and len(data['children']) > 0:  # 如果存在children并且children不是空列表
        if isinstance(data['children'][0], dict):  # 如果children的第元素是字典类型，即还有更深层的嵌套结构
            return get_first_child(data['children'][0])  # 继续深入
        else:
            return data['children'][0]  # 如果children的第元素不是字典类型，即已经达到最深层，返回该元素
    elif isinstance(data, str):
        return data  # 如果是字符串类型就直接返回
    else:
        return ""  # 如果不存在children或children是空列表，返回空字符串


# 目标文件夹
# 存放代码的公共文件夹
# (当前文件的上三级目录)等价于r"C:\MyCode"
code_dir = os.path.abspath(os.path.join(os.getcwd(), "../../../.."))
target_dir = code_dir + r"\TsLearn\my-page\docs"

# 创建一个空字典
my_sidebar: dict[str, bool | list | str] = {}  # 侧边栏
my_navbar = []  # 导航栏


def get_dir_json(dir_name: str, navbar_tit: str) -> None:
    """调用对应函数，并写入到侧边栏与导航栏的配置中
    """
    files_list = list_files(target_dir + "/" + dir_name)
    my_sidebar[f"/{dir_name}/"] = files_list['children']  # 向字典中放入一个键值对
    # 配置导航栏
    my_navbar.append({
        "text": navbar_tit,
        "link": get_first_child(files_list['children'][0])
    })


# javaLearn的文件夹输出结构
get_dir_json(r"javaLearn", "Java")
# tsLearn的文件夹输出结构
get_dir_json(r"tsLearn", "TS")
# pyLearn的文件夹输出结构
get_dir_json(r"pyLearn", "Python")

# 把dict转换为json字符串
pprint(my_sidebar)
sidebar_json_str = json.dumps(my_sidebar, ensure_ascii=False)
# 导航栏转json
pprint(my_navbar)
navbar_json_str = json.dumps(my_navbar, ensure_ascii=False)

# 然后写入侧边栏
with open(target_dir + r"\.vuepress\mySidebar.json", 'w', encoding="utf-8") as f:
    f.write(sidebar_json_str)
print("文件mySidebar.json内容替换成功")
# 再写入导航栏
with open(target_dir + r"\.vuepress\myNavbar.json", 'w', encoding="utf-8") as f:
    f.write(navbar_json_str)
print("文件myNavbar.json内容替换成功")
