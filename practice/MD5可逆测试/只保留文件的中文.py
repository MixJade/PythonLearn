# coding=utf-8
# @Time    : 2025/12/6 10:39
# @Software: PyCharm
import re


def remove_non_chinese(input_file, output_file):
    """
    去除TXT文件中的所有非中文内容，只保留中文汉字和中文标点
    :param input_file: 输入TXT文件路径（如"corpus_original.txt"）
    :param output_file: 输出纯中文TXT文件路径（如"corpus_cleaned.txt"）
    """
    # 定义匹配中文（含汉字+中文标点）的正则表达式
    # 范围说明：
    # \u4E00-\u9FFF：常用汉字
    chinese_pattern = re.compile(r'[^\u4E00-\u9FFF]')

    try:
        # 读取原始文件（UTF-8编码，若文件是GBK编码可改为encoding="gbk"）
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换所有非中文内容为空字符串
        cleaned_content = chinese_pattern.sub('', content)
        # 去除多余的空白行/空格
        cleaned_content = '\n'.join([line.strip() for line in cleaned_content.split('\n') if line.strip()])

        # 写入过滤后的内容到新文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        print(f"处理完成！纯中文内容已保存到：{output_file}")
        print(f"原始内容长度：{len(content)} 字符")
        print(f"过滤后内容长度：{len(cleaned_content)} 字符")

    except FileNotFoundError:
        print(f"错误：未找到文件 {input_file}")
    except UnicodeDecodeError:
        print(f"错误：文件编码不是UTF-8，尝试修改encoding参数为'gbk'或'gb2312'")
    except Exception as e:
        print(f"处理出错：{str(e)}")


# ========== 示例使用 ==========
if __name__ == "__main__":
    # 替换为你的输入/输出文件路径
    INPUT_FILE = "../outputFile/39007.txt"  # 原始带非中文的文件
    OUTPUT_FILE = "../outputFile/只留中文_结果.txt"  # 过滤后的纯中文文件

    remove_non_chinese(INPUT_FILE, OUTPUT_FILE)
