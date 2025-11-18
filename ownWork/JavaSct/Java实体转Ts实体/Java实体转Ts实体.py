# coding=utf-8
# @Time    : 2025/3/10 9:59
# @Software: PyCharm
import re
import subprocess


def convert_java_to_js(java_code):
    """将Java实体转换为ts类格式

    :param java_code: 使用lambok的Java实体类
    :return: 前端class格式的ts实体类
    """
    # 提取类名
    class_name_match = re.search(r'public class (\w+)', java_code)
    if not class_name_match:
        return None
    class_name = class_name_match.group(1)

    # 提取属性信息
    attribute_pattern = r'private (\w+) (\w+);'
    attributes = re.findall(attribute_pattern, java_code)

    # 生成 TypeScript 类代码
    ts_code = f"export class {class_name} {{\n"
    for _, attr_name in attributes:
        ts_code += f"  {attr_name}: string;\n"

    ts_code += "\n  constructor(\n    options: {\n"
    for _, attr_name in attributes:
        ts_code += f"      {attr_name}?: string;\n"
    ts_code += "    } = {}\n  ) {\n"
    for _, attr_name in attributes:
        ts_code += f"    this.{attr_name} = options.{attr_name} || \"\";\n"
    ts_code += "  }\n}"

    return ts_code


# 从文件中读取 Java 代码
with open('Java实体.txt', 'r', encoding='utf-8') as file:
    java_txt_code = file.read()

    # 转换并输出结果
    js_code = convert_java_to_js(java_txt_code)
    if js_code:
        print(js_code)
        # 将去除注释的结果放入剪贴板
        process = subprocess.Popen('clip', stdin=subprocess.PIPE, close_fds=True)
        process.communicate(input=js_code.encode())
        print("\n结果已复制到剪贴板")
    else:
        print("未找到有效的 Java 类定义。")
