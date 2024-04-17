# coding=utf-8
# @Time    : 2024/4/12 16:27
# @Software: PyCharm
import os
import re


def process_file(infile: str) -> None:
    """将小说根据章节拆分成不同文件
    \n(章节判定依据：上方打了@MixJade注解)

    :param infile: 输入文件路径
    """
    content = remove_two_empty_lines(infile)
    chapter_num: int = 0
    is_tit: bool = False
    buffer = []
    for line in content:
        # 匹配"@MixJade"作为章节分段符
        if line.strip() == '@MixJade':
            is_tit = True
            if buffer:
                chapter_num += 1
                creat_file_by_cha(buffer, chapter_num)
                buffer = []

        else:
            # 当@MixJade被满足时，它之后的第一个非空行是新文件名
            if is_tit and line != "\n":
                buffer.append(line)
                is_tit = False
            elif not is_tit:
                buffer.append(line)

    # 最后一个"@MixJade"对应的章节
    if buffer:
        chapter_num += 1
        creat_file_by_cha(buffer, chapter_num)


def remove_two_empty_lines(infile: str) -> list[str]:
    """将文件中的超过两个的空行合并成两个，并去除其中的注释符号

    :param infile: 输入文件路径
    :return: 处理后的文本内容
    """
    with open(infile, 'r', encoding='utf-8') as f:
        o_content: list[str] = f.readlines()
    content = []
    empty_lines = 0
    for line in o_content:
        if line.strip() == '':
            empty_lines += 1
        else:
            empty_lines = 0
        if empty_lines <= 2:
            # 去除文本注释符号，如⑹
            content.append(re.sub(r'[①-⓿]', '', line))
    print(f"清理了{len(o_content) - len(content)}个冗余空行")
    return content


def creat_file_by_cha(buffer_str: list[str], cha_num: int) -> None:
    """通过章节名来写入新的文件

    :param buffer_str: 待写入的文件内容
    :param cha_num: 输出的章节名
    """
    dst_dir = r"../../outputFile/章节拆分/"
    # 如果目标文件夹不存在则自动新建
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    # 拼接文件名(章节号至少三位，不足部分用0补齐)
    chapter_name = f"第{cha_num :03d}章 {buffer_str[0].strip()}"
    print(chapter_name)
    file_name = dst_dir + chapter_name + ".txt"
    # 写入新文件
    with open(file_name, 'w', encoding='utf-8') as f:
        for buf_line in buffer_str:
            f.write(buf_line)


if __name__ == '__main__':
    input_filename = r"../../inputFile/文本处理/测试章节拆分.txt"
    # 通过章节拆分文件
    process_file(input_filename)
