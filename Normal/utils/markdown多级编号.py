# coding=utf-8
# @Time    : 2024/4/17 16:48
# @Software: PyCharm
import re


def process_markdown(input_file: str, output_file: str):
    """对md标题重新编号,目前只处理一级与二级标题
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


if __name__ == '__main__':
    input_file1 = input("请输入待调整编号的md文件:")
    if input_file1.endswith(".md"):
        output_file1 = input_file1.replace(".md", "_num.md")
        process_markdown(input_file1, output_file1)
        print("文件已自动编号")
    else:
        print("输入的不是md文件")
