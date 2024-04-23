# coding=utf-8
# @Time    : 2024/4/23 17:33
# @Software: PyCharm
from PIL import Image


def cut_img(file_path: str, x1: int, y1: int, x2: int, y2: int) -> None:
    # 打开一张图片
    img = Image.open(file_path)

    # 定义一个坐标的矩形元组，四个参数分别是左上角点的x坐标、左上角点的y坐标，右下角点的x坐标、右上角点的y坐标
    area = (x1, y1, x2, y2)
    # 使用crop函数进行裁切
    cropped_img = img.crop(area)

    # 保存裁切后的图片
    cropped_img.save(file_path)


if __name__ == '__main__':
    x_o, y_o, x_t, y_t = 0, 465, 1080, 1995
    print(f"当前点:{x_o},{y_o} {x_t},{y_t}")
    # x_o, y_o = input("输入第1个点的坐标,逗号分割,如:1,2:").split(',')
    # print(f"{x_o},{y_o}")
    # x_t, y_t = input("输入第2个点的坐标,逗号分割,如:1,2:").split(',')
    # print(f"{x_t},{y_t}")
    while True:
        random_string = input("请输入文件路径(输入0退出)：")
        if random_string == '0':
            break
        cut_img(random_string, x_o, y_o, x_t, y_t)
