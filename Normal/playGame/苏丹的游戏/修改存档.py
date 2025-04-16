# coding=utf-8
# @Time    : 2025/4/16 21:34
# @Software: PyCharm
import json
import os


def check_one_key(data, target_key, new_value):
    if target_key in data:
        print(f"键 {target_key} 由 {data[target_key]} 改为 {new_value}")
        data[target_key] = new_value
    else:
        print(f"错误：键 {target_key} 不存在于 JSON 文件中。")


def check_two_key(data, outer_key, inner_key, new_value):
    if outer_key in data:
        if inner_key in data[outer_key]:
            print(f"键 {outer_key}.{inner_key} 由 {data[outer_key][inner_key]} 改为 {new_value}")
            data[outer_key][inner_key] = new_value
        else:
            print(f"错误：内层键 {inner_key} 不存在于 {outer_key} 中。")
    else:
        print(f"错误：外层键 {outer_key} 不存在于 JSON 文件中。")


def check_array_key(data, card_id, new_value):
    if "cards" in data:
        if isinstance(data["cards"], list):
            for item in data["cards"]:
                if isinstance(item, dict) and 'id' in item and item['id'] == card_id:
                    # 修改 tag 属性
                    item['tag'] = new_value
                    print(f"id为{card_id}的 card tag 已修改:{new_value}")
                    break
            else:
                print(f"错误：未找到 id 为 {card_id} 的元素。")
        else:
            print(f"错误：JSON 数据不是一个数组。")
    else:
        print("错误：键 cards 不存在于 JSON 文件中。")


def modify_json_key(file_path):
    try:
        # 读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 全局变量
        check_one_key(data, "sudan_card_init_life", 99)  # 苏丹卡时间
        check_two_key(data, "counter", "7100006", 99)  # 金骰子

        # 主角属性
        main_tag = {"physique": 100, "charm": 100, "battle": 100, "wisdom": 100, "magic": 100, "social": 100,
                    "conceal": 100, "survival": 100}
        check_array_key(data, 2000001, main_tag)
        check_array_key(data, 2000861, main_tag)

        # 随从属性
        adherent_tag = {"physique": 100, "charm": 100, "battle": 100, "wisdom": 100, "magic": 100, "social": 100,
                        "conceal": 100, "survival": 100, "adherent": 1, "support": 5}
        check_array_key(data, 2000006, adherent_tag)  # 普通老婆
        check_array_key(data, 2000458, adherent_tag)  # 强化老婆
        check_array_key(data, 2000372, adherent_tag)  # 法拉杰
        check_array_key(data, 2000461, adherent_tag)  # 贝姬夫人
        check_array_key(data, 2000460, adherent_tag)  # 哈桑
        check_array_key(data, 2000459, adherent_tag)  # 马尔基娜
        check_array_key(data, 2000129, adherent_tag)  # 阿图娜尔
        check_array_key(data, 2000019, adherent_tag)  # 热娜

        # 物品属性
        own_tag = {"physique": 100, "charm": 100, "battle": 100, "wisdom": 100, "magic": 100, "social": 100,
                   "conceal": 100, "survival": 100, "own": 1}
        check_array_key(data, 2000521, own_tag)  # 魅力护符
        check_array_key(data, 2000520, own_tag)  # 再生护符
        check_array_key(data, 2000368, own_tag)  # 家传宝甲

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
