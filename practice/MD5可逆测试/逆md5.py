# coding=utf-8
# @Time    : 2025/12/6 10:20
# @Software: PyCharm
import hashlib
import random

"""
测试MD5的部分可逆性：
看使用一个任意长度的中英文字符串，能否逆向生成md5匹配的中文字符

结论：即使尝试一亿次也不可能实现部分逆向
"""


# 生成随机中文的辅助函数（基于Unicode编码范围）
def generate_random_chinese(length=4):
    """生成指定长度的随机中文字符串"""
    chinese_chars = []
    # 常用中文字符的Unicode范围（0x4E00-0x9FFF）
    for _ in range(length):
        # 随机选取一个中文字符的Unicode编码
        code = random.randint(0x4E00, 0x9FFF)
        chinese_chars.append(chr(code))
    return ''.join(chinese_chars)


def find_chinese_md5_prefix(target_prefix, text_length=5, max_attempts=10000000):
    """
    查找前n位MD5匹配目标前缀的中文文本
    :param target_prefix: 目标MD5前缀（字符串）
    :param text_length: 生成的中文文本长度
    :param max_attempts: 最大尝试次数，防止无限循环
    :return: 匹配的中文文本，若未找到返回None
    """
    # 统一转为小写（MD5结果大小写不敏感）
    target_prefix = target_prefix.lower()

    for attempt in range(max_attempts):
        # 生成随机中文文本
        chinese_text = generate_random_chinese(text_length)

        # 计算MD5值（注意编码：中文需用utf-8）
        md5_result = hashlib.md5(chinese_text.encode('utf-8')).hexdigest().lower()

        # 对比前n位
        if md5_result == target_prefix[:len(md5_result)]:
            print(f"找到匹配文本！尝试次数：{attempt + 1}")
            print(f"中文文本：{chinese_text}")
            print(f"MD5值：{md5_result}")
            return chinese_text

    print(f"超出最大尝试次数（{max_attempts}），未找到匹配文本")
    return None


# ========== 示例使用 ==========
if __name__ == "__main__":
    # 目标MD5前缀（示例：假设你要匹配前8位）
    target_md5_prefix = "F79066DF57"  # 这是"123456"的MD5完整值：e10adc3949ba59abbe56e057f20f883e

    # 调用函数查找
    find_chinese_md5_prefix(target_md5_prefix)
