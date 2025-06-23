# coding=utf-8
# @Time    : 2025/6/23 11:16
# @Software: PyCharm


def remove_lines_with_pattern(lines, pattern, skip_num):
    """删除包含特定字符串的行，且连带删除后续特定数量的行
    :param lines: 输入文件字符串
    :param pattern: 特定的字符串
    :param skip_num: 需要跳过的后续行
    """
    new_lines = []
    skip_lines = 0

    for line in lines:
        if skip_lines > 0:
            skip_lines -= 1
            continue
        if pattern in line:
            skip_lines = skip_num  # 跳过后续3行
            new_lines.append("\n")  # 插入一个空行
            continue
        new_lines.append(line)

    return new_lines


# 使用示例
if __name__ == "__main__":
    input_file = '测试日志02.txt'  # 输入文件路径

    # 读取文件
    with open(input_file, 'r', encoding='utf-8') as f:
        old_lines = f.readlines()

    # 删除包含DELETE_ME的行，且连带删除后续3行
    new_lines_1 = remove_lines_with_pattern(old_lines, 'DELETE_ME', 3)

    # 最后写入新文件
    with open(input_file, 'w', encoding='utf-8') as f2:
        f2.writelines(new_lines_1)
    print(f"处理完成，结果已保存至 {input_file}")
