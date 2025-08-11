# coding=utf-8
# @Time    : 2025/4/1 14:32
# @Software: PyCharm
import re
import subprocess


def java_to_ts(java_str: str) -> str | None:
    """java代码转ts接口

    :param java_str: java代码的字符串
    :return: ts代码字符串
    """
    # 提取类名
    class_name_match = re.search(r'public class (\w+)', java_str)
    if class_name_match:
        class_name = class_name_match.group(1)
    else:
        print("未找到类名")
        return

    # 提取字段信息
    field_pattern = r'private (\w+) (\w+);'
    fields = re.findall(field_pattern, java_str)

    # 生成TypeScript接口
    ts_str = f"export interface {class_name} {{\n"
    for field_type, field_name in fields:
        if field_type == "Integer" or field_type == "BigDecimal":
            ts_type = "number"
        elif field_type == "Boolean":
            ts_type = "boolean"
        elif field_type == "String" or field_type == "LocalDate":
            ts_type = "string"
        else:
            ts_type = field_type  # 其他类型保持原样
        ts_str += f"    {field_name}: {ts_type};\n"
    ts_str += "}"

    return ts_str


# 读取Java代码文件
file_path = input("请输入java实体类路径:")
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        java_code = file.read()
    # 转换为TypeScript接口
    ts_interface = java_to_ts(java_code)
    if ts_interface:
        print(ts_interface)
        # 结果放入剪贴板
        process = subprocess.Popen('clip', stdin=subprocess.PIPE, close_fds=True)
        process.communicate(input=ts_interface.encode())
        print("去除注释后的xml已复制到剪贴板")
except FileNotFoundError:
    print(f"文件 {file_path} 未找到")
