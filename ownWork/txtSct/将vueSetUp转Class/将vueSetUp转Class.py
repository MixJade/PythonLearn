# coding=utf-8
# @Time    : 2025/12/11 10:24
# @Software: PyCharm
import re


def replace_value_with_this(code_segment: str) -> str:
    """将代码片段中的xxx.value替换为this.xxx"""
    pattern = r"(\w+)\.value"
    return re.sub(pattern, r"this.\1", code_segment)


def replace_no_type_val(code: str, ref_pattern: str) -> str:
    """处理ref定义（不带泛型）"""
    while True:
        match = re.search(ref_pattern, code, re.DOTALL)
        if not match:
            break
        var_name, var_value = match.groups()
        # 替换已处理的代码
        new_str = f"{var_name} = {var_value};"
        code = code[:match.start()] + new_str + code[match.end():]
    return code


def replace_type_val(code: str, ref_pattern: str) -> str:
    """处理ref定义（带泛型）"""
    while True:
        match = re.search(ref_pattern, code, re.DOTALL)
        if not match:
            break
        var_name, var_type, var_value = match.groups()
        # 替换已处理的代码
        new_str = f"{var_name} :{var_type} = {var_value};"
        code = code[:match.start()] + new_str + code[match.end():]
    return code


def transform_setup_to_js_class(original_code: str) -> str:
    """将Vue3的setup函数代码转换为JS类形式的代码"""
    code = original_code.strip()

    # 处理ref定义（带泛型）
    ref_pattern = r"const\s+(\w+)\s*=\s*ref<(\w+)>\((.*?)\);"
    code = replace_type_val(code, ref_pattern)

    # 处理ref定义（不带泛型）
    ref_pattern2 = r"const\s+(\w+)\s*=\s*ref\((.*?)\);"
    code = replace_no_type_val(code, ref_pattern2)

    # 处理reactive定义（带泛型）
    reactive_pattern = r"const\s+(\w+)\s*:\s*([\w\[\]]+)\s*=\s*reactive\(([\s\S]*?)\);"
    code = replace_type_val(code, reactive_pattern)

    # 处理reactive定义（不带泛型）
    reactive_pattern2 = r"const\s+(\w+)\s*=\s*reactive\(([\s\S]*?)\);"
    code = replace_no_type_val(code, reactive_pattern2)

    # 处理普通const变量
    normal_const_pattern = r"const\s+(\w+)\s*=\s*({.*?});"
    code = replace_no_type_val(code, normal_const_pattern)

    # 处理箭头函数
    arrow_func_pattern = r"const\s+(\w+)\s*=\s*\((.*?)\)\s*=>\s*({[\s\S]*?});"
    while True:
        match = re.search(arrow_func_pattern, code, re.DOTALL)
        if not match:
            break
        func_name, func_params, func_body = match.groups()
        # 替换函数体内的.value
        new_str = f"{func_name}({func_params}){func_body}"
        code = code[:match.start()] + new_str + code[match.end():]

    # 处理剩余代码中的.value和proxy.
    code = replace_value_with_this(code)
    code = code.replace("proxy.", "this.")
    return code


if __name__ == "__main__":
    with open(r"样例setup.txt", 'r', encoding='utf-8') as file:
        original_setup_code = file.read()
        transformed_code = transform_setup_to_js_class(original_setup_code)
        with open(r"样例setup转换_结果.txt", 'w', encoding='utf-8') as file2:
            file2.write(transformed_code)
        print(f"\n======= 转换后的JS类代码已输出 =======")
