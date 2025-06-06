# coding=utf-8
# @Time    : 2025/4/21 9:53
# @Software: PyCharm
import random
import string
from datetime import datetime, timedelta

# 百家姓
surnames = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁荀羊於惠甄麴家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴鬱胥能苍双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍卻璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡国文寇广禄阙东殴殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾毋沙乜养鞠须丰巢关蒯相查后荆红游竺权逯盖益桓公万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空亓官司寇仉督子车颛孙端木巫马公西漆雕乐正壤驷公良拓拔夹谷宰父谷梁晋楚闫法汝鄢涂钦段干百里东郭南门呼延归海羊舌微生岳帅缑亢况后有琴梁丘左丘东门西门商牟佘佴伯赏南宫墨哈谯笪年爱阳佟"
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


if __name__ == "__main__":
    name, gender_1 = generate_name()
    id_number = generate_id_number(gender_1)
    bank_name_1, card_number_1 = generate_bank_card()
    print(f"姓名: {name}")
    print(f"性别: {gender_1}")
    print(f"身份证号: {id_number}")
    print(f"手机号: {generate_phone_number()}")
    print(f"开户行: {bank_name_1}")
    print(f"银行卡号: {card_number_1}")
