# coding=utf-8
# @Time    : 2025/6/23 13:43
# @Software: PyCharm
from datetime import datetime


def extract_timestamp(line):
    """从行中提取前23个字符作为时间戳"""
    return line[:23] if len(line) >= 23 else line


def parse_timestamp(timestamp_str):
    """将时间戳字符串解析为datetime对象"""
    try:
        return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
    except ValueError:
        return None


def calculate_time_difference(timestamp1, timestamp2):
    """计算两个时间戳之间的毫秒差"""
    if not timestamp1 or not timestamp2:
        return None
    delta = timestamp2 - timestamp1
    return delta.total_seconds() * 1000  # 转换为毫秒


def process_logs(log_content: list[str], begin_str: str, end_str: str, end_next_num=0) -> list[int]:
    """处理日志内容，提取所有匹配组合并计算时间差

    :param log_content: 日志内容
    :param begin_str: 接口开始的关键字符串，其所在行需有时间戳
    :param end_str: 接口结束的关键字符串
    :param end_next_num: 是否从接口结束的关键字符串后面几行取值
    """
    param_lines = []  # 存储包含begin_str的行
    stmt_lines = []  # 存储包含end_str的行

    # 遍历日志行，收集匹配的行
    for i in range(len(log_content)):
        line = log_content[i]
        if begin_str in line:
            param_lines.append(line)
        if end_str in line:
            if end_next_num == 0:
                # 无下一行索取直接添加
                stmt_lines.append(line)
            else:
                # 否则添加下一行
                next_line = log_content[i + end_next_num]
                stmt_lines.append(next_line)  # 将下一行添加到stmt_lines

    # 按顺序配对并计算时间差
    results = []
    for i in range(min(len(param_lines), len(stmt_lines))):
        timestamp1 = extract_timestamp(param_lines[i])
        timestamp2 = extract_timestamp(stmt_lines[i])
        # 解析时间戳
        ts1 = parse_timestamp(timestamp1)
        ts2 = parse_timestamp(timestamp2)
        # 计算时间差
        time_diff = calculate_time_difference(ts1, ts2)
        results.append(time_diff)

    return results


def analysis_res(title: str, results: list[int]) -> None:
    """分析接口耗时的分析结果"""
    print("-" * 50)
    print(title)
    if not results:
        print("未找到匹配的组合")
    else:
        print(f"共{len(results)}次调用,总耗时{sum(results):.2f} 毫秒")
        # 挨个输出
        # for res in results:
        #     print(f"  时间差: {res:.2f} 毫秒")
        # 求最大值
        print(f"最长耗时: {max(results):.2f} 毫秒")
        # 求平均耗时
        average = sum(results) / len(results)
        print(f"平均时长: {average:.2f} 毫秒")


if __name__ == '__main__':
    input_file = '测试日志03.txt'  # 输入文件路径

    # 读取文件
    with open(input_file, 'r', encoding='utf-8') as f:
        old_lines = f.readlines()

    # 处理日志并打印结果
    analysis_res("接口一", process_logs(old_lines, "第一接口开始", "第一接口结束"))
    analysis_res("接口2", process_logs(old_lines, "二接口开始", "第二接口返回报文", 1))
