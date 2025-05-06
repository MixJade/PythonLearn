# coding=utf-8
# @Time    : 2025/5/6 11:22
# @Software: PyCharm
try:
    # 打开文件
    with open('../../outputFile/destination2.txt', 'r', encoding='utf-8') as file:
        # 读取文件全部内容
        content = file.read()
        print(content)
except FileNotFoundError:
    print("错误：文件未找到。")
except Exception as e:
    print(f"发生未知错误：{e}")
