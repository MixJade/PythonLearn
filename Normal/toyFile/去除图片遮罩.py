# coding=utf-8
# @Time    : 2025/7/14 15:29
# @Software: PyCharm
import os
import sys
from pathlib import Path

from PIL import Image


def format_color(r: float) -> int:
    return max(0, min(round(r), 255))


def calculate_base_color(final_color, overlay_color=(0, 0, 0), alpha=0.88):
    """
    根据最终颜色、遮罩颜色和透明度反向计算基底颜色

    参数:
    final_color: 最终颜色，是RGB元组
    overlay_color: 遮罩颜色，是RGB元组
    alpha: 遮罩透明度(0.0-1.0)，0表示透明，1表示不透明

    返回:
    基底颜色的RGB元组
    """

    # 验证透明度范围
    if not (0.0 <= alpha <= 1.0):
        raise ValueError("透明度必须在0.0到1.0之间")

    # 处理alpha=1的特殊情况
    if alpha == 1:
        if final_color == final_color:
            return None, "无法确定基底颜色（遮罩不透明且最终颜色等于遮罩颜色）"
        else:
            raise ValueError("无效的颜色组合：当透明度为1时，最终颜色必须等于遮罩颜色")

    # 计算基底颜色
    r = (final_color[0] - overlay_color[0] * alpha) / (1 - alpha)
    g = (final_color[1] - overlay_color[1] * alpha) / (1 - alpha)
    b = (final_color[2] - overlay_color[2] * alpha) / (1 - alpha)

    return format_color(r), format_color(g), format_color(b)


def replace_color(input_path, output_path):
    """
    将图片中特定颜色的像素替换为新颜色

    参数:
    input_path (str): 输入图片路径
    output_path (str): 输出图片路径
    """
    try:
        # 打开图片
        with Image.open(input_path) as img:
            # 转换为RGB模式（如果是PNG等可能是RGBA模式）
            img = img.convert("RGB")
            width, height = img.size

            # 创建新的图片对象
            new_img = Image.new("RGB", (width, height))

            # 遍历每个像素
            for y in range(height):
                for x in range(width):
                    # 获取当前像素颜色
                    current_pixel = img.getpixel((x, y))
                    # 替换颜色
                    new_img.putpixel((x, y), calculate_base_color(current_pixel))

            # 保存修改后的图片
            new_img.save(output_path)
            print(f"图片处理完成，已保存至 {output_path}")

    except Exception as e1:
        print(f"处理图片时出错: {e1}")
        sys.exit(1)


def hex_to_rgb(hex_color):
    """将十六进制颜色代码转换为RGB元组"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("无效的十六进制颜色代码，应为6个字符（不包括#）")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


if __name__ == "__main__":
    # 输入图片，这里的遮罩图片可以找`TsLearn\h5\demo\css测试\遮罩测试.html`自行截图
    input_img: str = os.path.join(os.path.expanduser("~"), f"Desktop/Test32.jpg")
    # 输出图片路径，默认为输入图片同级文件夹
    input_file = Path(input_img)
    output_file = input_file.parent / f"{input_file.stem}_结果{input_file.suffix}"
    output_img = str(output_file)

    # 执行颜色替换
    replace_color(input_img, output_img)
