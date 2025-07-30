# coding=utf-8
# @Time    : 2025/5/19 9:05
# @Software: PyCharm
def count_characters(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # 过滤掉换行符、空格和制表符
            filtered_content = content.replace('\n', '').replace(' ', '').replace('\t', '')
            return len(filtered_content)
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在")
        return 0
    except Exception as e:
        print(f"错误：读取文件时发生异常 - {e}")
        return 0


if __name__ == "__main__":
    file_path_1 = r"testData/测试章节拆分.txt"
    count = count_characters(file_path_1)
    print(f"文件中有效字符（不含换行、空格、制表符）数量为：{count}")
