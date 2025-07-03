# coding=utf-8
# @Time    : 2025/7/3 10:02
# @Software: PyCharm
import os


def replace_in_files(file_paths, search_string, replace_string):
    """
    批量替换多个文件中的字符串

    参数:
    file_paths (list): 要处理的文件路径列表
    search_string (str): 要查找的字符串
    replace_string (str): 替换字符串
    """
    for file_path in file_paths:
        if not os.path.isfile(file_path):
            print(f"错误: 文件 '{file_path}' 不存在")
            continue

        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # 替换字符串
            if search_string in content:
                new_content = content.replace(search_string, replace_string)

                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)

                print(f"已替换文件: {file_path}")
            else:
                print(f"文件 '{file_path}' 中未找到目标字符串")
        except Exception as e:
            print(f"处理文件 '{file_path}' 时出错: {e}")


if __name__ == "__main__":
    files_path = []  # 要处理的文件路径列表
    search_txt = '保留第一次出现的重复行'  # 要处理的文件路径列表"
    replace_txt = '保留第1次出现的重复行'  # 替换字符串

    file_dir = "../从csv提取字段去重"
    files_name = ['csv分组输出.py', 'csv提取大类去重.py']
    for i in range(0, len(files_name)):
        files_path.append(os.path.join(file_dir, files_name[i]))

    # 最后替换(如果要换回去的话，可调整此处参数位置)
    replace_in_files(files_path,
                     search_txt,
                     replace_txt
                     )
