# coding=utf-8
# @Time    : 2024/3/11 9:19
# @Software: PyCharm
import re


def replace_img_text(img_text: str) -> str:
    """图片md格式的字符串替换为【图片】

    :param img_text: 图片md格式字符串,形如:![xxx](xxx)
    :return: 【图片】
    """
    # 使用正则表达式替换
    return re.sub(r'!\[.*]\(.*\)', '【图片】', img_text)


print(replace_img_text('![xxx](xxx)'))  # 输出：【图片】
