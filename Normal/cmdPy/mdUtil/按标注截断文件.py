# coding=utf-8
# @Time    : 2025-01-16 09:13:26
# @Software: PyCharm

target1 = '【此行以上皆删】'  # 向上删除注解
target2 = '【此行以下皆删】'  # 向下删除注解


def delete_lines(filename: str) -> None:
    """
    删除target1之前的所有行,删除target2之后的所有行

    :param filename: 文件路径
    """
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        up_index, down_index = 0, len(lines)
        i = -1
        for line in lines:
            i = i + 1
            # 如果找到向上删除注解
            if line.strip() == target1:
                up_index = i
            # 如果找到向下删除注解
            elif line.strip() == target2:
                if i < down_index:
                    down_index = i
        if up_index == 0 and down_index == len(lines):
            print("没有注解")
        elif up_index > down_index:
            print("注解位置有误")
        else:
            if up_index != 0:
                up_index += 1  # 如果有这个注解就删掉它
            with open(filename, 'w', encoding='utf-8') as wf:  # 以写入模式打开文件
                wf.writelines(lines[up_index:down_index])  # 写入指定的行


# 使用函数,
if __name__ == '__main__':
    print(f"1. 在文件中标注 {target1} 会删除其上所有行")
    print(f"2. 在文件中标注 {target2} 会删除其下所有行")
    input_file1 = input("输入打了标记的文本文件:").strip('"')
    delete_lines(input_file1)
