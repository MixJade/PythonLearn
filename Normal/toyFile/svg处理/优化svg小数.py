# coding=utf-8
# @Time    : 2025/3/25 14:36
# @Software: PyCharm
import re


def round_svg_decimals(svg_content):
    # 正则表达式匹配带符号的浮点数（包括负号）
    pattern = r'(-?\d+\.\d+)'

    # 替换函数：将匹配到的字符串转为浮点数，四舍五入保留整数
    def replace_match(match):
        num = float(match.group())
        return f"{num:.0f}"

    # 进行替换
    return re.sub(pattern, replace_match, svg_content)


# 处理并输出结果
svg_path: str = input("请输入需要去除注释的svg路径: ")

with open(svg_path, 'r', encoding='utf-8') as f:
    content = f.read()
    # 处理并输出结果
    processed_svg = round_svg_decimals(content)
    print(processed_svg)

# 以写入模式打开文件，将处理后的内容写回文件
with open(svg_path, 'w', encoding='utf-8') as f:
    f.write(processed_svg)
print("SVG文件已成功更新")
