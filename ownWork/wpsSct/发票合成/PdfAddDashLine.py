# coding=utf-8
# @Time    : 2026/4/15 15:28
# @Software: PyCharm
import io
import os

import fitz  # pymupdf
from PIL import Image

"""
合并后的PDF添加横向虚线

1. 固定分割线位置：148.4mm ~ 150.4mm（上下部分分界）
2. 每个区域：第一条虚线 = 内容区域顶部边界上1mm，第二条虚线 = 第一条+12.6cm
"""

# 转换比例
DPI = 300  # 用于检测的DPI
MM_TO_INCH = 1 / 25.4

# 虚线参数 (mm)
LINE_INTERVAL_MM = 126  # 126mm（本来应该是120mm的，但是打印机会默认缩放95%）
CONTENT_OFFSET_MM = 1  # 内容往上1mm

# 固定分割线位置 (mm)
DIVIDER_TOP_MM = 148.4  # 分割线顶部
DIVIDER_BOTTOM_MM = 150.4  # 分割线底部


def pdf_page_to_image(page, dpi=300):
    """将PDF页面转换为图像"""
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    return Image.open(io.BytesIO(img_data))


def get_pixel_size(img):
    """获取图像像素尺寸"""
    return img.width, img.height


def find_content_boundary_top(img, start_y_px=0):
    """从指定位置往下查找第一个有内容的行

    :param img: PIL图像对象
    :param start_y_px: 起始像素Y坐标（从此位置往下搜索）
    :return: 边界像素Y坐标，如果没有找到则返回None
    """
    width, height = get_pixel_size(img)

    for y in range(start_y_px, height):
        row = img.crop((0, y, width, y + 1))
        pixels = list(row.getdata())
        # 检查是否有非白色像素
        has_content = any(
            p[0] < 250 or p[1] < 250 or p[2] < 250
            for p in pixels
        )
        if has_content:
            return y
    return None


def pixels_to_mm(pixels, dpi=300):
    """像素转换为毫米"""
    return pixels / (dpi * MM_TO_INCH)


def mm_to_points(mm):
    """毫米转换为PDF点"""
    return mm * 72 / 25.4


def draw_dashed_line(page, y_pt, width_pt, color=(0, 0, 0)):
    """在PDF页面绘制横向虚线"""
    dash_length_pt = 8  # 划线长度 (pt)
    gap_length_pt = 5  # 间隔长度 (pt)

    x = 0  # 从页面边缘开始
    while x < width_pt:
        end_x = min(x + dash_length_pt, width_pt)
        page.draw_line(
            fitz.Point(x, y_pt),
            fitz.Point(end_x, y_pt),
            color=color,
            width=0.75
        )
        x += dash_length_pt + gap_length_pt


def add_dashed_lines(page, line1_mm, line2_mm):
    """在指定位置绘制两条虚线

    :param page: PDF页面对象
    :param line1_mm: 第一条虚线位置(mm)
    :param line2_mm: 第二条虚线位置(mm)
    """
    page_width_pt = page.rect.width
    page_height_pt = page.rect.height
    # 转换为点
    line1_pt = mm_to_points(line1_mm)
    line2_pt = mm_to_points(line2_mm)
    # 确保虚线在页面范围内
    line1_pt = max(10, min(line1_pt, page_height_pt - 10))
    line2_pt = max(10, min(line2_pt, page_height_pt - 10))
    # 绘制虚线（黑色）
    draw_dashed_line(page, line1_pt, page_width_pt, color=(0, 0, 0))
    draw_dashed_line(page, line2_pt, page_width_pt, color=(0, 0, 0))


def process_region(page, img, region_name: str, start_y_px: int, search_end_px: int):
    """处理一个区域：在该区域查找内容边界，添加两条虚线

    :param page: PDF页面对象
    :param img: PIL图像对象
    :param region_name: 区域名称（用于日志）
    :param start_y_px: 搜索起始像素Y坐标
    :param search_end_px: 搜索结束像素Y坐标
    :return: (line1_mm, line2_mm) 或 None（如果无内容）
    """
    # 查找内容区域顶部边界
    content_y_px = find_content_boundary_top(img, start_y_px)
    # 检查是否超出搜索范围或无内容
    if content_y_px is None or content_y_px >= search_end_px:
        print(f"    {region_name}: 无内容")
        return None
    content_y_mm = pixels_to_mm(content_y_px)
    region_bottom_mm = pixels_to_mm(search_end_px)  # 区域底部边界（mm）
    # 计算初始虚线位置
    line1_mm = content_y_mm - CONTENT_OFFSET_MM  # 内容上1mm
    line2_mm = line1_mm + LINE_INTERVAL_MM        # 第一条往下12.6cm

    print(f"    {region_name}:")
    print(f"      内容起始: {content_y_mm:.1f}mm")
    print(f"      区域底部: {region_bottom_mm:.1f}mm")
    print(f"      第一条虚线: {line1_mm:.1f}mm (内容上{CONTENT_OFFSET_MM}mm)")
    print(f"      第二条虚线: {line2_mm:.1f}mm")

    # 触底检测：若第二条虚线超出区域底部，则整体向上移1mm，循环直到不触底
    shift_count = 0
    while line2_mm > region_bottom_mm:
        shift_count += 1
        line1_mm -= 1.0
        line2_mm -= 1.0
        print(f"      [触底调整 {shift_count}] 整体上移1mm → 第一条: {line1_mm:.1f}mm, 第二条: {line2_mm:.1f}mm")

    # 绘制虚线
    add_dashed_lines(page, line1_mm, line2_mm)
    return line1_mm, line2_mm


def process_pdf(pdf_path, output_path):
    """处理单个PDF文件"""
    print(f"\n处理: {os.path.basename(pdf_path)}")

    doc = fitz.open(pdf_path)
    output_doc = fitz.open(pdf_path)

    for page_num, page in enumerate(output_doc):
        print(f"  处理第 {page_num + 1} 页...")

        # 将页面转换为图像用于分析
        img = pdf_page_to_image(page, dpi=DPI)
        width_px, height_px = get_pixel_size(img)

        # 转换为毫米
        page_width_mm = pixels_to_mm(width_px)
        page_height_mm = pixels_to_mm(height_px)
        print(f"    页面尺寸: {page_width_mm:.1f}mm x {page_height_mm:.1f}mm")
        print(f"    分割线位置: {DIVIDER_TOP_MM}mm ~ {DIVIDER_BOTTOM_MM}mm")

        # 计算分割线在像素单位下的位置
        divider_top_px = DIVIDER_TOP_MM * DPI * MM_TO_INCH
        divider_bottom_px = DIVIDER_BOTTOM_MM * DPI * MM_TO_INCH

        # === 处理上半部分 ===
        process_region(
            page, img,
            region_name="上半部分",
            start_y_px=0,
            search_end_px=int(divider_top_px)
        )

        # === 处理下半部分 ===
        process_region(
            page, img,
            region_name="下半部分",
            start_y_px=int(divider_bottom_px),
            search_end_px=int(height_px)
        )

    # 保存处理后的PDF
    output_doc.save(output_path, garbage=4, deflate=True)
    output_doc.close()
    doc.close()

    print(f"  已保存: {os.path.basename(output_path)}")


def main():
    """主函数"""
    # 通过input获取PDF文件路径
    pdf_path = input("请输入PDF文件路径: ").strip().strip('"')

    # 检查文件是否存在
    if not os.path.isfile(pdf_path):
        print(f"文件不存在: {pdf_path}")
        return

    # 检查是否为PDF文件
    if not pdf_path.lower().endswith('.pdf'):
        print("请输入PDF文件!")
        return

    # 生成输出路径：文件名前加 "dash_"
    directory = os.path.dirname(pdf_path)
    filename = os.path.basename(pdf_path)
    output_filename = "dash_" + filename
    output_path = os.path.join(directory, output_filename) if directory else output_filename

    print(f"\n输入文件: {pdf_path}")
    print(f"输出文件: {output_path}")
    print(f"\n虚线逻辑:")
    print(f"  - 分割线位置: {DIVIDER_TOP_MM}mm ~ {DIVIDER_BOTTOM_MM}mm")
    print(f"  - 第一条虚线: 内容区域顶部边界上{CONTENT_OFFSET_MM}mm")
    print(f"  - 第二条虚线: 第一条往下12cm ({LINE_INTERVAL_MM}mm)")

    try:
        process_pdf(pdf_path, output_path)
        print("\n" + "=" * 50)
        print("处理完成!")
    except Exception as e:
        print(f"\n处理失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
