# coding=utf-8
# @Time    : 2024/4/25 10:29
# @Software: PyCharm
from PIL import Image


def resize_image(img_path: str) -> None:
    """转换图片尺寸,不合比例的会进行一定裁剪

    :param img_path: 待转换尺寸的图片路径
    """
    # 读取文件宽高
    img = Image.open(img_path)
    width, height = img.size
    print(f"图片宽高为:{width, height}")

    # 查看比例是否正常
    t_ratio = t_width / t_height
    ratio = width / height
    # 按照比例裁剪图片
    if t_ratio > ratio:
        print("当前比例小于目标:高度过大")
        new_height = width / t_ratio
        print(width / new_height)
        x1, x2 = 0, width
        y1 = (height - new_height) / 2
        y2 = y1 + new_height
        # 使用crop函数进行裁切
        area = (x1, int(y1), x2, int(y2))
        print(f"裁剪目标点:{area}")
        img = img.crop(area)
    elif t_ratio < ratio:
        print("当前比例大于目标:宽度过大")
        new_width = t_ratio * height
        print(new_width / height)
        y1, y2 = 0, height
        x1 = (width - new_width) / 2
        x2 = x1 + new_width
        # 使用crop函数进行裁切
        area = (int(x1), y1, int(x2), y2)
        print(f"裁剪目标点:{area}")
        img = img.crop(area)
    else:
        print("当前比例与目标一致")

    # 转换图片尺寸
    resized_image = img.resize((t_width, t_height))
    resized_image.save(img_path)
    print("转换完成")


if __name__ == '__main__':
    # 目标宽高
    t_width, t_height = 1920, 1080
    print(f"目标宽高为:{t_width, t_height}")
    while True:
        filename = input("输入图片路径(0退出/1重设宽高):")
        if filename == '0':
            break
        elif filename == '1':
            print("""=========================
    方案1 [1920 1080]
    方案2 [128 128]
    其它n 自定义宽高
=========================""")
            plan_str = input("请选择你的方案:")
            if plan_str == '1':
                t_width, t_height = 1920, 1080
            elif plan_str == '2':
                t_width, t_height = 128, 128
            else:
                # 输入格式如: 1 2
                t_width, t_height = input("输入目标宽高,空格分割:").split(' ')
            print(f"目标宽高为:{t_width, t_height}")
        else:
            filename = filename.strip('"')  # 去除首尾可能存在的双引号
            resize_image(filename)
