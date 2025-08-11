# coding=utf-8
# @Time    : 2025/4/21 9:53
# @Software: PyCharm
import random
import string
import json
from datetime import datetime, timedelta

# 百家姓
with open("chinese_surnames.json", 'r', encoding='utf-8') as f:
    surnames = json.load(f)
# 中文数字
chinese_numbers = "一二三四五六七八九十"


# 随机生成姓名和性别
def generate_name():
    surname = random.choice(surnames)
    name_length = len(str(random.randint(1, 99)))
    given_name = ''.join(random.choice(chinese_numbers) for _ in range(name_length))
    gender = random.choice(['男', '女'])
    return surname + given_name, gender


# 随机生成身份证号
def generate_id_number(gender):
    # 生成合理的出生日期（1900年至今）
    start_date = datetime(1900, 1, 1)
    end_date = datetime.now()
    random_days = random.randint(0, (end_date - start_date).days)
    birth_date = start_date + timedelta(days=random_days)
    # 格式化出生日期为YYYYMMDD
    birth_date_str = birth_date.strftime('%Y%m%d')
    # 前6位地区码（随机生成,最小为1）
    area_code = ''.join(random.choices(string.digits[1:], k=6))
    # 顺序码（第15-17位）
    sequential_code = ''.join(random.choices(string.digits, k=2))
    # 调整第17位数字以符合性别
    if gender == '男':
        gender_digit = str(random.choice([1, 3, 5, 7, 9]))
    else:
        gender_digit = str(random.choice([0, 2, 4, 6, 8]))
    # 组合前17位
    first_17_digits = area_code + birth_date_str + sequential_code + gender_digit
    # 加权因子
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 校验码对应值
    check_code_list = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    # 计算校验码
    total = sum(int(a) * b for a, b in zip(first_17_digits, weights))
    check_code = check_code_list[total % 11]
    return first_17_digits + check_code


# 随机生成银行卡号及开户行名称
def generate_bank_card():
    banks = {
        "中国工商银行": "622202",
        "中国农业银行": "622848",
        "中国银行": "621661",
        "中国建设银行": "622700",
        "交通银行": "622260"
    }
    bank_name = random.choice(list(banks.keys()))
    bank_prefix = banks[bank_name]
    # 生成剩余的卡号数字
    remaining_digits = ''.join(random.choices(string.digits, k=19 - len(bank_prefix)))
    card_number = bank_prefix + remaining_digits
    return bank_name, card_number


def generate_phone_number():
    # 定义中国手机号的前缀
    prefixes = [
        '130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
        '145', '147', '149',
        '150', '151', '152', '153', '155', '156', '157', '158', '159',
        '166',
        '170', '171', '172', '173', '175', '176', '177', '178',
        '180', '181', '182', '183', '184', '185', '186', '187', '188', '189',
        '191', '198', '199'
    ]
    # 随机选择一个前缀
    prefix = random.choice(prefixes)
    # 生成后面的8位随机数字
    suffix = ''.join(random.choices('0123456789', k=8))
    # 组合成完整的手机号
    return prefix + suffix


def generate_random_email():
    """
    随机生成QQ邮箱、网易邮箱或Gmail邮箱

    返回:
        str: 随机生成的邮箱地址
    """
    # 定义邮箱域名列表
    domains = [
        "qq.com",  # QQ邮箱
        "163.com",  # 网易163邮箱
        "126.com",  # 网易126邮箱
        "yeah.net",  # 网易yeah邮箱
        "gmail.com"  # Gmail邮箱
    ]

    # 随机选择一个域名
    domain = random.choice(domains)

    # 根据不同域名生成合适的用户名
    if domain == "qq.com":
        # QQ邮箱用户名为纯数字，长度9-12位
        username_length = random.randint(9, 12)
        username = ''.join(random.choices(string.digits, k=username_length))
    else:
        # 其他邮箱用户名可以包含字母、数字和下划线，长度6-15位
        username_chars = string.ascii_letters + string.digits + '_'
        username_length = random.randint(6, 15)
        username = ''.join(random.choices(username_chars, k=username_length))

    # 组合成完整邮箱
    return f"{username}@{domain}"


def main():
    name, gender_1 = generate_name()
    id_number = generate_id_number(gender_1)
    bank_name_1, card_number_1 = generate_bank_card()
    print(f"姓名: {name}")
    print(f"性别: {gender_1}")
    print(f"身份证号: {id_number}")
    print(f"手机号: {generate_phone_number()}")
    print(f"邮箱: {generate_random_email()}")
    print(f"开户行: {bank_name_1}")
    print(f"银行卡号: {card_number_1}")
    print()


if __name__ == "__main__":
    main()
    try:
        while True:
            in_y = input("-->键入Y继续: ")
            if in_y.upper() == 'Y':
                main()
            else:
                print("退出程序")
                break
    except KeyboardInterrupt:
        # 捕获Ctrl+C导致的KeyboardInterrupt异常
        print("\n用户中断操作，程序退出")
