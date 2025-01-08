import re


def convert(name: str) -> str:
    """
    将大蛇形转为小驼峰
    :param name: 形如 ORJ_NAME
    :return: prjName
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    res1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    words = [word.capitalize() for word in res1.split('_')]
    result = ''.join(words)
    result = result[0].lower() + result[1:]
    return result


with open('ibatis的插入列.txt', 'r') as file:
    for line in file:
        if line.endswith(",\n"):
            print(f'{line[:-2]}=#{convert(line[:-2])}#,\n', end='')
        else:
            print(f'{line}=#{convert(line)}#', end='')
