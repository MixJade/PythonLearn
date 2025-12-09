# coding=utf-8
# @Time    : 2025/11/25 14:54
# @Software: PyCharm
import os
import json
from utils.genDateId import get_time_id


def batch_replace_file_content(root_folder: str, replace_map: dict[str, str]) -> None:
    """
    批量替换文件夹下所有文件的内容

    :param root_folder: 目标文件夹路径（绝对/相对路径均可）
    :param replace_map: 替换规则字典，格式：{待替换字符串: 目标字符串}
    """
    # 遍历文件夹
    for root, dirs, files in os.walk(root_folder):
        for filename in files:
            # 拼接文件完整路径
            file_path = os.path.join(root, filename)

            # 读取文件内容
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # 标记是否有替换操作
            replaced = False
            operator_map = {}
            # 执行批量替换（按 replace_map 中的规则）
            for old_str, new_str in replace_map.items():
                if old_str in content:
                    content = content.replace(old_str, new_str)
                    replaced = True
                    operator_map[old_str] = new_str

            # 若有替换，写入新内容（覆盖原文件）
            if replaced:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"已替换：{file_path}")
                for old_str, new_str in operator_map.items():
                    print(f"\t{old_str} --> {new_str}")
            else:
                print(f"无匹配内容：{file_path}")


def modify_form_id_in_json(root_folder: str, replace_map: dict[str, str], filename_list: list[str]) -> dict[str, str]:
    """
    读取文件中的特定属性值，并返回新的替换规则
    """
    i = 0
    for read_filename in filename_list:
        # 1. 读取JSON文件
        file_path = os.path.join(root_folder, read_filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 2. 遍历数据
        if isinstance(data, list):  # 确保顶层是列表
            for item in data:
                if isinstance(item, dict):
                    if 'layoutId' in item and item['layoutId'] not in replace_map:
                        i += 1
                        replace_map[item['layoutId']] = "123" + get_time_id(i)
                    if 'formFieldId' in item:
                        i += 1
                        replace_map[item['formFieldId']] = "123" + get_time_id(i)
        # 3. 返回新的规则map
        return replace_map


# ------------------- 示例调用 -------------------
if __name__ == "__main__":
    # 1. 配置参数
    TARGET_FOLDER = "测试压缩文件夹_结果"  # 待处理的文件夹路径
    REPLACE_RULES = {
        # 这里只是formId的替换
        "first_old_formId": "first_new_formId",
        "second_old_formId": "second_new_formId",
    }
    # 2. 从以下json中提取需要替换的主键
    READ_FILENAME_LIST = ["desFormLayout.json", "desFormControl.json"]
    REPLACE_RULES = modify_form_id_in_json(TARGET_FOLDER, REPLACE_RULES, READ_FILENAME_LIST)
    # 3. 执行批量替换
    batch_replace_file_content(root_folder=TARGET_FOLDER, replace_map=REPLACE_RULES)

    print("\n批量替换完成！留意文件：" + "、".join(READ_FILENAME_LIST))
