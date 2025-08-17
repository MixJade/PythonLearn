# coding=utf-8
# @Time    : 2024/12/15 9:38
# @Software: PyCharm
import os

from PIL import Image


def change_extensions(folder_path, end_suffix):
    """批量改后缀
    """
    # 检查目录下是否存在子目录
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            print(f"错误：目录 '{folder_path}' 包含子目录 '{item}'，拒绝执行")
            return

    # 获取目录下的所有文件
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # 处理文件扩展名
    for filename in files:
        old_path = os.path.join(folder_path, filename)
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}.{end_suffix}"
        new_path = os.path.join(folder_path, new_filename)

        try:
            os.rename(old_path, new_path)
            print(f"已重命名: {old_path} -> {new_path}")
        except Exception as e:
            print(f"无法重命名 '{old_path}': {e}")


def turn_webp(folder_path):
    """转换webp为jpg
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".webp"):
            print(f"{filename} 已转化")
            img = Image.open(os.path.join(folder_path, filename)).convert("RGB")
            img.save(os.path.join(folder_path, filename[:-5] + '.jpg'), "jpeg")
            os.remove(os.path.join(folder_path, filename))  # 删除.webp文件


if __name__ == '__main__':
    # 获取图片文件夹下所有图片
    file_path = input("输入目标文件夹下某个图片路径：").strip('"')
    # 获取文件路径
    dir_path = os.path.dirname(file_path)
    # 选择功能
    print("=" * 50)
    print("输入1转换文件夹下所有webp为jpg")
    print("输入2转换文件夹下所有文件名后缀改为webp")
    print("其它输入则终止程序")
    print("=" * 50)
    choose = input("请选择: ")
    if choose == "1":
        turn_webp(dir_path)
    elif choose == "2":
        change_extensions(dir_path, "webp")
    else:
        print("程序已结束")
