# coding=utf-8
# @Time    : 2025/12/6 10:44
# @Software: PyCharm
import hashlib


def split_text_by_4_chars(input_file, output_file):
    """
    将文本文件按每4个字符截取为一行，生成新文件
    :param input_file: 输入文本文件路径
    :param output_file: 输出截取后的文件路径
    """
    try:
        # 读取文件内容，去除原有的换行符（避免干扰截取）
        with open(input_file, 'r', encoding='utf-8') as f:
            # 读取所有内容并替换换行符为空白，确保文本连续
            content = f.read().replace('\n', '').replace('\r', '')

        # 按每4个字符切分文本
        # 切片语法：content[i:i+4] 从索引i开始取4个字符，直到文本末尾
        split_lines = [content[i:i + 4] for i in range(0, len(content), 4)]
        # 直接丢弃最后一行
        if split_lines:  # 防止列表为空时报错
            split_lines.pop()  # 删除最后一个元素

        # 遍历生成md5
        for i in range(len(split_lines)):
            # 获取当前行文本
            line_text = split_lines[i]
            # 拼接文本+MD5，并更新原列表的对应位置
            split_lines[i] = line_text + hashlib.md5(line_text.encode('utf-8')).hexdigest().lower()

        # 将切分后的内容写入新文件，每行一个4字符片段
        with open(output_file, 'w', encoding='utf-8') as f:
            # 用换行符连接所有片段，写入文件
            f.write('\n'.join(split_lines))

        print(f"处理完成！文件已保存至：{output_file}")
        print(f"原始文本长度：{len(content)} 字符")
        print(f"截取后总行数：{len(split_lines)} 行")

    except FileNotFoundError:
        print(f"错误：未找到文件 {input_file}")
    except UnicodeDecodeError:
        print(f"错误：文件编码不是UTF-8，尝试修改encoding参数为'gbk'")
    except Exception as e:
        print(f"处理出错：{str(e)}")


# ========== 示例使用 ==========
if __name__ == "__main__":
    # 替换为你的输入/输出文件路径
    INPUT_FILE = "../outputFile/只留中文_结果.txt"  # 纯中文文本文件
    OUTPUT_FILE = "../outputFile/语料库_结果.txt"  # 按4字符分行的文件

    split_text_by_4_chars(INPUT_FILE, OUTPUT_FILE)
