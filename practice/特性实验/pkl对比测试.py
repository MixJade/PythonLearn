# coding=utf-8
# @Time    : 2025/7/29 10:44
# @Software: PyCharm
import json
import pickle
from pathlib import Path


def save_list_json(data_list, file_path):
    """使用JSON格式保存列表"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            # 确保中文正常显示
            json.dump(data_list, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"JSON保存失败: {e}")
        return False


def load_list_json(file_path):
    """从JSON文件读取列表"""
    try:
        if not Path(file_path).exists():
            return []

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"JSON读取失败: {e}")
        return []


def save_list_pickle(data_list, file_path):
    """使用Pickle格式保存列表（二进制）"""
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(data_list, f)
        return True
    except Exception as e:
        print(f"Pickle保存失败: {e}")
        return False


def load_list_pickle(file_path):
    """从Pickle文件读取列表"""
    try:
        if not Path(file_path).exists():
            return []

        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Pickle读取失败: {e}")
        return []


# 使用示例
if __name__ == "__main__":
    # 创建一个包含中文的示例列表
    chinese_list = [f"测试元素{i}：中文内容示例" for i in range(1000)]

    # 保存列表
    save_list_json(chinese_list, "chinese_list_结果.json")
    save_list_pickle(chinese_list, "chinese_list_结果.pkl")

    # 读取列表
    loaded_json = load_list_json("chinese_list_结果.json")
    loaded_pickle = load_list_pickle("chinese_list_结果.pkl")

    print(f"JSON读取到 {len(loaded_json)} 个元素，第1个元素 {loaded_json[0]}")
    print(f"Pickle读取到 {len(loaded_pickle)} 个元素，第2个元素 {loaded_pickle[1]}")
