# coding=utf-8
# @Time    : 2024/9/17 11:37
# @Software: PyCharm

def align_text(title_str: str, max_len: int) -> str:
    """返回加入了占位符的文字

    :param title_str: 需要处理的中英文混合字符串
    :param max_len: 格式化后的最大长度(按英文空格计数)
    :return: 最终格式化后的字符串
    """
    for j in str(title_str):
        if '\u4e00' <= j <= '\u9fff':
            max_len = max_len - 1
    # 中文占两个字符,英文占一个,所以最终长度应该为(总长度-中文数)
    # 左对齐,并填充字符串
    return title_str.ljust(max_len, ' ')


if __name__ == '__main__':
    test_data = [
        ["张三zs123", 23],
        ["张三12", 523],
        ["李四94", 3],
        ["星星9527.py", 223],
        ["马云jkm996", 23],
    ]
    print(f"{align_text('姓名', 20)}年龄")
    for i in test_data:
        print(f"{align_text(i[0], 20)}{i[1]}")
