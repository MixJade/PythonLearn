# coding=utf-8
# @Time    : 2025/3/20 16:41
# @Software: PyCharm
import os
from PIL import Image


def remove_metadata(input_path, output_path):
    try:
        # 打开图片
        image = Image.open(input_path)

        # 创建一个没有元数据的新图片对象
        # noinspection PyTypeChecker
        new_image = Image.new(image.mode, image.size)
        new_image.putdata(list(image.getdata()))

        # 保存新图片
        new_image.save(output_path)
        print(f"图片元数据已成功去除")
        print(f"原文件大小: {os.path.getsize(input_path)} 字节, 新文件大小: {os.path.getsize(output_path)} 字节")
    except Exception as e:
        print(f"处理图片时出错: {e}")


def replace_last_s(s):
    # 从字符串末尾开始查找 . 的位置
    last_index = s.rfind('.')
    if last_index != -1:
        # 若找到 s，则进行替换
        return s[:last_index] + '.out' + s[last_index:]
    return s


if __name__ == "__main__":
    print("去除图片元数据")
    while True:
        filename = input("输入图片路径(0退出):")
        if filename == '0' or filename == '':
            break
        else:
            filename = filename.strip('"')  # 去除首尾可能存在的双引号
            out_filename = replace_last_s(filename)
            remove_metadata(filename, out_filename)
