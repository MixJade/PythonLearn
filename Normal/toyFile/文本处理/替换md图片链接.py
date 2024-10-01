# coding=utf-8
# @Time    : 2024/3/11 9:24
# @Software: PyCharm
import re


def replace_md_img_text(path: str) -> None:
    """图片md格式的字符串替换为【图片】

    :param path: 文件路径
    """
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(path, 'w', encoding='utf-8') as file:
        for line in lines:
            # 使用正则表达式替换
            # 图片md格式(形如:![xxx](xxx))的字符串替换为【图片】
            new_line = re.sub(r'!\[.*]\(.*\)', '【图片】', line)
            file.write(new_line)


replace_md_img_text(r"data/特殊md文件/没有标题的md.md")
