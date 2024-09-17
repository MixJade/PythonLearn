# coding=utf-8
# @Time    : 2024/9/17 11:37
# @Software: PyCharm
def is_chinese(ch: str) -> bool:
    if '\u4e00' <= ch <= '\u9fff':
        return True
    return False


def align_text(title_key: str, max_english: int) -> str:
    """返回加入了占位符的文字"""
    chinese_count = 0
    english_count = 0
    for j in str(title_key):
        if is_chinese(j):
            chinese_count = chinese_count + 1
        else:
            english_count = english_count + 1

    temp = max_english - english_count
    while temp > 0:
        title_key = title_key + ' '
        temp = temp - 1
    title_key = title_key.ljust(7, chr(12288))
    return title_key


if __name__ == '__main__':
    test_data = [
        ["张三123", 23],
        ["张三12", 523],
        ["李四94", 3],
        ["星星9527", 223],
        ["马云996", 23],
    ]
    print(f"{align_text('姓名', 10)}年龄")
    for i in test_data:
        print(f"{align_text(i[0], 10)}{i[1]}")
