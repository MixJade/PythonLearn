# coding=utf-8
# @Time    : 2024/3/2 13:14
# @Software: PyCharm
def replace_content_in_two_lines(file_path: str, start_str: str, end_str: str, content: str) -> None:
    """替换文件指定两行间的内容

    :param file_path: 文件路径
    :param start_str: 起始行的字符串(包含就行)
    :param end_str: 结束行的字符串(包含就行)
    :param content: 所写入的内容
    """
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    # 对应起始、结束字符串的索引
    start_index = next(index for index, line in enumerate(lines) if start_str in line)  # 找到起始行
    end_index = next(index for index, line in enumerate(lines) if end_str in line)  # 找到结束行

    # 替换指定行的内容
    lines[start_index + 1:end_index] = [content]
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # 最后输出结果
    print(f"文件:‘{file_path}’的内容替换成功")


if __name__ == '__main__':
    replace_content_in_two_lines("testData/有标题但不匹配的md.md",
                                 start_str="// 天地自然，秽炁分散。",
                                 end_str="// 乾罗答那，洞罡太玄；",
                                 content="新的内容")
