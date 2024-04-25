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
    while True:
        random_string = input("输入文件路径(0退出/1重设坐标)：")
        if random_string == '0' or random_string == '':
            break
        elif random_string == '1':
            print("""=========================
    方案1 [0,465 1080,1995]
    方案2 [0,0 1440,810]
    其它n 自定义坐标
=========================""")
            plan_str = input("请选择你的方案:")
            if plan_str == '1':
                x_o, y_o, x_t, y_t = 0, 465, 1080, 1995
            elif plan_str == '2':
                x_o, y_o, x_t, y_t = 0, 0, 1440, 810
            else:
                # 输入格式如: 1 2
                x_o, y_o = input("输入第1个点的坐标,空格分割:").split(' ')
                x_t, y_t = input("输入第2个点的坐标,空格分割:").split(' ')
            print(f"当前点:{x_o},{y_o} {x_t},{y_t}")
        else:
            cut_img(random_string.strip('"'), x_o, y_o, x_t, y_t)
