# coding=utf-8
# @Time    : 2025/7/21 15:34
# @Software: PyCharm
import re


def camel_to_snake(snake_str: str) -> str:
    """将小驼峰转为大蛇形

    :param snake_str: 形如 prj_name
    :return: PRJ_NAME
    """
    # 用于存储转换后的字符列表
    snake_case = []
    for i, char in enumerate(snake_str):
        # 若当前字符是大写字母，并且不是字符串的第一个字符
        if char.isupper() and i > 0:
            # 前一个字符是小写字母或数字时添加下划线
            if snake_str[i - 1].islower() or snake_str[i - 1].isdigit():
                snake_case.append('_')
        # 把当前字符添加到结果列表
        snake_case.append(char)
    # 把列表组合成字符串并转为大写
    return ''.join(snake_case).upper()


def snake_to_camel(name: str) -> str:
    """将大蛇形转为小驼峰

    :param name: 形如 ORJ_NAME
    :return: prjName
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    res1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    words = [word.capitalize() for word in res1.split('_')]
    result = ''.join(words)
    result = result[0].lower() + result[1:]
    return result


def small_snake_to_camel(snake_str):
    """将小蛇形转为小驼峰

    :param snake_str: 形如 prj_name
    :return: prjName
    """
    components = snake_str.split('_')
    # 第一个单词保持小写，其余单词首字母大写
    return components[0] + ''.join(x.title() for x in components[1:])


def snake_to_big_camel(name: str) -> str:
    """将大蛇形转为大驼峰

    :param name: 形如 ORJ_NAME
    :return: PrjName
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    res1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    words = [word.capitalize() for word in res1.split('_')]
    return ''.join(words)
