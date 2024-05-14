# coding=utf-8
# @Time    : 2024/4/17 16:48
# @Software: PyCharm
import re


# noinspection DuplicatedCode
def process_markdown(input_file: str, output_file: str):
    """(处理小说)对md标题重新编号,目前只处理到三级标题
    """
    results = []
    # 标题顺序
    first_title_num = 0
    second_title_num = 0
    third_title_num = 0
    # 标题编号匹配表达式
    pattern1 = re.compile(r'# 第\d+章 (.*)')
    pattern2 = re.compile(r'## \d+\.\d+ (.*)')
    pattern3 = re.compile(r'### \d+\.\d+.\d+ (.*)')
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            # 匹配一级标题
            if line.startswith('# '):
                first_title_num += 1
                second_title_num = 0
                # 判断该章节标题是否已经被标号
                if pattern1.match(line):
                    tit_name = re.search(pattern1, line).group(1)
                    new_line = f'# 第{first_title_num}章 {tit_name}\n'
                else:
                    new_line = f'# 第{first_title_num}章 {line[2:]}'
                results.append(new_line)
            # 匹配二级标题
            elif line.startswith('## '):
                second_title_num += 1
                # 判断该章节标题是否已经被标号
                if pattern2.match(line):
                    tit_name = re.search(pattern2, line).group(1)
                    new_line = f'## {first_title_num}.{second_title_num} {tit_name}\n'
                else:
                    new_line = f'## {first_title_num}.{second_title_num} {line[3:]}'
                results.append(new_line)
            # 匹配三级标题
            elif line.startswith('### '):
                third_title_num += 1
                # 判断该章节标题是否已经被标号
                if pattern3.match(line):
                    tit_name = re.search(pattern3, line).group(1)
                    new_line = f'### {first_title_num}.{second_title_num}.{third_title_num} {tit_name}\n'
                else:
                    new_line = f'### {first_title_num}.{second_title_num}.{third_title_num} {line[3:]}'
                results.append(new_line)
            else:
                results.append(line)
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in results:
            file.write(line)


# noinspection DuplicatedCode
def process_markdown2(input_file: str):
    """(处理笔记)对md标题重新编号,专门处理笔记
    """
    results = []
    # 标题顺序
    first_title_num = 0
    second_title_num = 0
    third_title_num = 0
    # 标题编号匹配表达式
    pattern1 = re.compile(r'## [一二三四五六七八九十百]+、(.*)')
    pattern2 = re.compile(r'### \d+\.\d+ (.*)')
    pattern3 = re.compile(r'#### \d+\.\d+.\d+ (.*)')
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            # 匹配二级标题
            if line.startswith('## '):
                first_title_num += 1
                second_title_num = 0
                if pattern1.match(line):
                    tit_name = re.search(pattern1, line).group(1)
                    new_line = f'## {turn_num_to_chinese(first_title_num)}、{tit_name}\n'
                else:
                    new_line = f'## {turn_num_to_chinese(first_title_num)}、{line[2:]}'
                results.append(new_line)
            # 匹配三级标题
            elif line.startswith('### '):
                second_title_num += 1
                if pattern2.match(line):
                    tit_name = re.search(pattern2, line).group(1)
                    new_line = f'### {first_title_num}.{second_title_num} {tit_name}\n'
                else:
                    new_line = f'### {first_title_num}.{second_title_num} {line[3:]}'
                results.append(new_line)
            # 匹配四级标题
            elif line.startswith('#### '):
                third_title_num += 1
                if pattern3.match(line):
                    tit_name = re.search(pattern3, line).group(1)
                    new_line = f'#### {first_title_num}.{second_title_num}.{third_title_num} {tit_name}\n'
                else:
                    new_line = f'#### {first_title_num}.{second_title_num}.{third_title_num} {line[3:]}'
                results.append(new_line)
            else:
                results.append(line)
    with open(input_file, 'w', encoding='utf-8') as file:
        for line in results:
            file.write(line)


def turn_num_to_chinese(num: int) -> str:
    """将数字转为中文
    """
    num_str = str(num)
    trans_dict = {'0': '零', '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八',
                  '9': '九'}
    unit_dict = {1: '', 2: '十', 3: '百'}
    res = ""
    for i in range(len(num_str)):
        res += trans_dict[num_str[i]]
        if len(num_str) - i != 1 and num_str[i] != '0':
            res += unit_dict[len(num_str) - i]
    if res.startswith("一十"):
        res = res.lstrip("一")  # 移除开头的一
    if res.endswith("零"):
        res = res.rstrip("零")  # 移除末尾的零
    return res


if __name__ == '__main__':
    print("方案1:处理小说；方案2:处理笔记")
    check_type: str = input("请选择你的方案：")
    if check_type == '1':
        print("处理小说")
        input_file1 = input("请输入待调整编号的md文件:").strip('"')
        if input_file1.endswith(".md"):
            output_file1 = input_file1.replace(".md", "_num.md")
            process_markdown(input_file1, output_file1)
            print("文件已自动编号")
        else:
            print("输入的不是md文件")
    else:
        print("处理笔记")
        input_file1 = input("请输入待调整编号的md文件:").strip('"')
        if input_file1.endswith(".md"):
            process_markdown2(input_file1)
            print("文件已自动编号")
        else:
            print("输入的不是md文件")
