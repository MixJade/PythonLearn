# coding=utf-8
# @Time    : 2024/4/24 12:20
# @Software: PyCharm
import os
from PIL import Image

filename = input("输入png文件路径:")
ext = os.path.splitext(filename)[1]
if ext == ".PNG" or ext == ".png":
    img = Image.open(filename)
    rgb_im = img.convert('RGB')
    output_file = filename.replace("ext", ".jpg")
    # 保存jpg图片时设置质量为75%
    rgb_im.save(output_file, quality=75)
else:
    print("输入文件格式不正确")


