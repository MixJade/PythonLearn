# coding=utf-8
# @Time    : 2024/12/15 9:38
# @Software: PyCharm
import os

from PIL import Image

# 获取图片文件夹下所有图片
file_path = input("输入目标文件夹下某个图片路径：").strip('"')
# 获取文件路径
folder_path = os.path.dirname(file_path)

for filename in os.listdir(folder_path):
    if filename.endswith(".webp"):
        img = Image.open(os.path.join(folder_path, filename)).convert("RGB")
        img.save(os.path.join(folder_path, filename[:-5] + '.jpg'), "jpeg")
        os.remove(os.path.join(folder_path, filename))  # 删除.webp文件
