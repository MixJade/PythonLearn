import re


def extract_attributes(file_path):
    """取出文件中的所有属性值

    :param file_path: 文件路径
    :return: 属性值列表
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # 使用正则表达式匹配属性定义
    pattern = r'private\s+\w+\s+(\w+)\s*;'
    attributes = re.findall(pattern, content)
    return set(attributes)


def find_different_attributes(file1_old, file2_new):
    """ 找两个java实体类文件的差异

    :param file1_old: 较旧的实体类
    :param file2_new: 较新的实体类
    :return: [旧有新无的属性, 新有旧无的属性]
    """
    attributes1 = extract_attributes(file1_old)
    attributes2 = extract_attributes(file2_new)

    # 找出不同的属性
    different_attributes_1 = (attributes1 - attributes2)
    different_attributes_2 = (attributes2 - attributes1)
    return different_attributes_1, different_attributes_2


if __name__ == "__main__":
    file1_path = "旧java实体.txt"
    file2_path = "新java实体.txt"

    different_attributes = find_different_attributes(file1_path, file2_path)

    print("旧有新无的属性:")
    for attribute in different_attributes[0]:
        print(attribute)
    print("新有旧无的属性:")
    for attribute in different_attributes[1]:
        print(attribute)
