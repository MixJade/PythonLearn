# coding=utf-8
# @Time    : 2025-01-16 09:13:26
# @Software: PyCharm


def delete_lines(filename: str) -> None:
    """
    删除 @MixJade Up 行之前的所有行,删除 @MixJade Down 之后的所有行

    :param filename: 文件路径
    """
    target1 = '@MixJade Up'  # 向上删除注解
    target2 = '@MixJade Down'  # 向下删除注解

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
            if line.strip() == target2:
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
    input_file1 = input("输入打了注解的日志文件:").strip('"')
    delete_lines(input_file1)
