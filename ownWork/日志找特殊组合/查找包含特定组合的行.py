# coding=utf-8
# @Time    : 2025/8/7 10:34
# @Software: PyCharm
def find_matching_lines(file_path: str, target1: str, target2: str):
    # 打开文件并逐行处理
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        # 读取第一行
        prev_line = file.readline()
        prev_line_number = 1

        # 总共匹配的行数
        matching_line_num = 0
        while True:
            current_line = file.readline()

            # 如果到达文件末尾，退出循环
            if not current_line:
                break

            # 检查条件：上一行包含"target1"且当前行包含"target2"
            if target1 in prev_line and target2 in current_line:
                matching_line_num += 1
                print(f"--- 第 {prev_line_number} 行符合条件 ---")
                print(f"    -> {prev_line}")

            # 更新上一行和行号，准备下一次循环
            prev_line = current_line
            prev_line_number += 1
        print(f"=== 共有 {matching_line_num} 行符合条件 ===")


if __name__ == "__main__":
    log_file_path = r"测试日志02.txt"
    print(f"正在分析文件: {log_file_path}")

    # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
    find_matching_lines(log_file_path, "INSERT INTO PRJ_OP_REL", "dog")
