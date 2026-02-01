# coding=utf-8
# @Time    : 2026/2/1 15:24
# @Software: PyCharm
import os

while True:
    # 接收用户输入的文件名
    file_name = input("请输入文件名（输入0退出程序）：").strip()
    # 判断是否输入0，若是则退出循环
    if file_name == "0" or not file_name:
        print("程序已退出。")
        break
    # 分割文件名和后缀（以最后一个.为分隔符，最多分割1次）
    if "." not in file_name:
        print("错误：若文件名无后缀。")
        break
    # rsplit从右侧开始分割，处理多后缀文件名更合理
    file_without_suffix, suffix = file_name.rsplit(".", 1)
    command = f'ffmpeg -i {file_name} {file_without_suffix}_01_frame.jpg'
    os.system(command=command)
    print(f"文件已保存至：{file_without_suffix}_01_frame.jpg")
    print("-" * 30)  # 分隔线，让输出更整洁
