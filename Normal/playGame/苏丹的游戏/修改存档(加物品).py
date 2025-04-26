# coding=utf-8
# @Time    : 2025/4/16 21:34
# @Software: PyCharm
import json
import os


def add_card(data, card_msgs: list):
    """给自己加一张卡片

    :param data: json数据
    :param card_msgs: 卡片的id和tag(列表)
    """
    begin_uid = data["card_uid_index"]

    if "cards" in data:
        if isinstance(data["cards"], list):
            for card_msg in card_msgs:
                data["cards"].append(
                    {"uid": begin_uid, "id": card_msg["id"], "count": card_msg["count"], "life": 1, "rareup": 0,
                     "tag": card_msg["tag"],
                     "equip_slots": [],
                     "equips": [], "bag": 3, "bagpos": 2, "custom_name": "", "custom_text": ""})
                begin_uid += 1
                data["card_uid_index"] = begin_uid
                print(f"新的卡片追加成功:{card_msg['id']}")
        else:
            print(f"错误：JSON 数据不是一个数组。")
    else:
        print("错误：键 cards 不存在于 JSON 文件中。")


def modify_json_key(file_path):
    try:
        # 读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 给自己加一张卡
        add_card(data, card_msgs=[
            {"id": 2000304, "tag": {"own": 1}, "count": 1},  # 小鳄鱼
            {"id": 2000304, "tag": {"own": 1}, "count": 1},  # 小鳄鱼
            {"id": 2000304, "tag": {"own": 1}, "count": 1},  # 小鳄鱼
            {"id": 2000304, "tag": {"own": 1}, "count": 1},  # 小鳄鱼
            {"id": 2000304, "tag": {"own": 1}, "count": 1},  # 小鳄鱼
            {"id": 2000304, "tag": {"own": 1}, "count": 1},  # 小鳄鱼
            {"id": 2000029, "tag": {}, "count": 60},  # 金币
        ])

        # 将修改后的数据写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"修改完成")

    except FileNotFoundError:
        print("错误：文件未找到。")
    except json.JSONDecodeError:
        print("错误：无法解析 JSON 文件。")
    except Exception as e:
        print(f"错误：发生未知错误：{e}")


# 获取 %userprofile% 的值
user_profile = os.getenv('USERPROFILE')
save_file_path = user_profile + r'\AppData\LocalLow\DoubleCross\SultansGame\SAVEDATA\76561197960287930\auto_save.json'
modify_json_key(save_file_path)
