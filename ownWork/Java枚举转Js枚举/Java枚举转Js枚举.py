# coding=utf-8
# @Time    : 2025/3/17 14:08
# @Software: PyCharm
def enum_java_to_js(java_enum: str) -> str:
    """将Java实体转换为ts类格式

    :param java_enum: java枚举(只有键值对)
    :return: 前端js枚举
    """
    # 提取枚举类名
    enum_name = None
    lines = java_enum.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith("public enum"):
            parts = line.split()
            enum_name = parts[2].split('{')[0]
            break

    # 提取枚举项
    enum_items = []
    for line in lines:
        line = line.strip()
        if '(' in line and ')' in line and not line.startswith('public enum'):
            parts = line.split('(')
            name = parts[0].strip()
            values = parts[1].replace(')', '').replace('"', '').split(',')
            code = values[0].strip()
            display_name = values[1].strip()
            enum_items.append((name, code, display_name))

    # 生成前端枚举
    js_enum = f"const {enum_name[0].lower() + enum_name[1:]} = {{\n"
    for name, code, display_name in enum_items:
        js_enum += f"  {name}: {{ code: \"{code}\", name: \"{display_name}\" }},\n"
    js_enum = js_enum.rstrip(',\n') + '\n};'

    return js_enum


# 从文件中读取 Java 代码
with open('Java枚举.txt', 'r', encoding='utf-8') as file:
    java_txt_enum = file.read()

    # 转换并输出结果
    js_code = enum_java_to_js(java_txt_enum)
    print(js_code)
