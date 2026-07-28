# coding=utf-8
# @Time    : 2026/07/15
# @Software: PyCharm
"""
探查 desFormControl.json 数据，输出为 Markdown 表格

输入支持：
  - zip 文件：自动解压后读取其中的 desFormControl.json
  - json 文件：直接读取 desFormControl.json

输出列：表单项 | 绑定属性 | 字典项 | 树形字典
"""

import os
import json
import tempfile
import shutil

from zip_util import unzip_file, validate_single_form_zip


# ===================== 读取 desFormControl.json =====================

def load_form_control(input_path: str) -> list:
    """
    从 zip 或 json 文件中读取 desFormControl.json 数据。

    :param input_path: zip 文件路径 或 desFormControl.json 文件路径
    :return: 控件列表
    """
    input_path = input_path.strip().strip('"').strip("'")

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"文件不存在：{input_path}")

    # ---- 输入是 zip ----
    if input_path.lower().endswith(".zip"):
        validate_single_form_zip(input_path)  # 先校验单表单，多表单直接拒绝
        print(f"检测到 zip 文件，正在解压读取 desFormControl.json ...")
        tmp_dir = tempfile.mkdtemp(prefix="form_inspect_")
        try:
            unzip_file(input_path, tmp_dir)
            json_path = os.path.join(tmp_dir, "desFormControl.json")
            if not os.path.exists(json_path):
                raise FileNotFoundError(f"zip 中未找到 desFormControl.json：{input_path}")
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        return data

    # ---- 输入是 json ----
    elif input_path.lower().endswith(".json"):
        print(f"读取 JSON 文件：{input_path}")
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    else:
        raise ValueError(f"不支持的文件类型，请输入 .zip 或 .json 文件：{input_path}")


# ===================== 输出 Markdown 表格 =====================

def to_markdown_table(data: list) -> str:
    """
    将 desFormControl.json 数据转为 Markdown 表格字符串。

    列：表单项 | 绑定属性 | 字典项 | 树形字典
    """
    lines = ["| 序号 | 表单项 | 绑定属性 | 字典项 | 树形字典 |",
             "|---|---|---|---|---|"]

    for idx, item in enumerate(data, 1):
        form_field_describe = item.get('formFieldDescribe', '') or '-'
        bound_property = item.get('boundProperty', '') or '-'
        general_dictionary = item.get('generalDictionary', '') or '-'
        tree_shape = item.get('treeShape', '') or '-'
        tree_shape = f"（树形）{tree_shape}" if tree_shape != '-' else tree_shape
        lines.append(f"| {idx} | {form_field_describe} | {bound_property} | {general_dictionary} | {tree_shape} |")

    lines.append("")
    lines.append(f"共 {len(data)} 条记录")
    return "\n".join(lines)


# ===================== 主流程 =====================

def run() -> str:
    """
    探查 desFormControl.json -> Markdown 表格。

    返回: 成功时返回输入的文件路径，失败时返回空字符串
    """
    print("=" * 50)
    print("  探查 desFormControl.json -> Markdown 表格")
    print("  (支持输入 zip 或 desFormControl.json)")
    print("=" * 50)

    input_path = input("\n请输入文件路径（zip 或 desFormControl.json）：").strip()
    if not input_path:
        print("未输入路径，退出。")
        return ""

    try:
        data = load_form_control(input_path)
    except Exception as e:
        print(f"[错误] {e}")
        return ""

    if not isinstance(data, list):
        print(f"[错误] desFormControl.json 顶层应为列表，实际为 {type(data).__name__}")
        return ""

    print()
    md_table = to_markdown_table(data)
    print(md_table)

    return input_path


if __name__ == "__main__":
    run()
