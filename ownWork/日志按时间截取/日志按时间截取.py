# coding=utf-8
# @Time    : 2025/8/7 14:57
# @Software: PyCharm
from datetime import datetime


def filter_logs_by_time(log_lines: list[str], start_time_str: str, end_time_str: str):
    """筛选指定时间范围内的日志

    :param log_lines: 日志文本内容
    :param start_time_str: 开始时间字符串（格式：YYYY-MM-DD HH:MM）
    :param end_time_str: 结束时间字符串（格式：YYYY-MM-DD HH:MM）
    :return: 符合时间范围的日志列表
    """
    # 转换时间字符串为datetime对象（精确到分钟）
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")

    filtered_logs = []

    print(f"开始截取 {start_time} 至 {end_time} 的日志")
    print("\t" * 5 + f"(当前时间 {datetime.now()})")
    for line in log_lines:
        # 提取日志中的时间戳（前19个字符：YYYY-MM-DD HH:MM:SS）
        if len(line) >= 19 and line[10] == ' ' and line[13] == ':' and line[16] == ':':
            try:
                log_time_str = line[:19]  # 截取时间部分（如"2025-04-03 16:28:41"）
                log_time = datetime.strptime(log_time_str, "%Y-%m-%d %H:%M:%S")

                # 筛选：>=开始时间 且 <结束时间
                if start_time <= log_time < end_time:
                    filtered_logs.append(line)
            except ValueError:
                # 忽略时间格式错误的行（非日志主体行）
                continue
        else:
            # 非时间开头的行（如日志内容换行），跟随前一条有效日志
            if filtered_logs:  # 如果已有筛选的日志，追加到最后一条
                filtered_logs[-1] += line
    return filtered_logs


# 示例用法
if __name__ == "__main__":
    input_file = r"测试截取日志.log"  # 输入文件路径

    if not input_file.endswith(".log"):
        print("请输入.log文件")
        exit(0)

    # 1. 读取日志内容
    with open(input_file, 'r', encoding='utf-8') as f:
        log_content = f.readlines()

    # 2. 筛选时间范围：2025-04-03 16:27 至 2025-04-03 16:31（不包括16:31）
    start = "2025-04-03 16:27"
    end = "2025-04-03 16:31"
    result = filter_logs_by_time(log_content, start, end)

    # 3. 输出结果
    # 最后写入新文件
    with open(input_file.replace(".log", "_结果.log"), 'w', encoding='utf-8') as f2:
        f2.writelines(result)
    print(f"处理完成，结果已保存至 {input_file}")
