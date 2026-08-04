# coding=utf-8
# @Time    : 2026/8/4
# @Software: PyCharm
import os

import fitz  # pymupdf

"""
PDF 页面内容缩放 —— 保持页面尺寸不变，将页面内容缩放到指定比例（默认 0.9）。
"""

SCALE = 0.9  # 内容缩放比例


def scale_pdf_content(input_path: str, output_path: str, scale: float = SCALE):
    """将 PDF 每一页的内容缩放到指定比例，页面尺寸保持不变，内容居中放置。

    :param input_path:  输入 PDF 路径
    :param output_path: 输出 PDF 路径
    :param scale:       内容缩放比例，0.9 = 缩小到90%
    """
    src_doc = fitz.open(input_path)
    out_doc = fitz.open()

    for page_idx in range(len(src_doc)):
        src_page = src_doc[page_idx]
        page_w = src_page.rect.width
        page_h = src_page.rect.height

        # 新建相同尺寸的空白页
        out_page = out_doc.new_page(width=page_w, height=page_h)

        # 计算缩放后的目标矩形（居中）
        scaled_w = page_w * scale
        scaled_h = page_h * scale
        offset_x = (page_w - scaled_w) / 2
        offset_y = (page_h - scaled_h) / 2
        target_rect = fitz.Rect(offset_x, offset_y, offset_x + scaled_w, offset_y + scaled_h)

        # 将原页面内容绘制到缩放后的区域
        out_page.show_pdf_page(target_rect, src_doc, page_idx, keep_proportion=True, overlay=True)

    out_doc.save(output_path, garbage=4, deflate=True)
    out_doc.close()
    src_doc.close()
    print(f"✅ 缩放完成（比例 {scale}）：{output_path}\n")


def build_output_path(input_path: str) -> str:
    """根据输入文件名生成输出文件名，保存在同目录下。"""
    base, ext = os.path.splitext(input_path)
    return f"{base}_scale{int(SCALE * 100)}{ext}"


def main():
    print("=" * 55)
    print(f"   PDF 页面内容缩放工具（比例 {SCALE}）")
    print("=" * 55)
    print("使用说明：")
    print("  · 输入 PDF 路径，可直接拖入文件")
    print("  · 输入 0 退出程序\n")

    while True:
        raw = input("请输入 PDF 路径（0=退出）：\n> ").strip()
        user_input = raw.strip('"').strip("'")

        if user_input == "0":
            print("👋 退出程序")
            break

        if not os.path.isfile(user_input):
            print(f"❌ 文件不存在，请重新输入：{user_input!r}\n")
            continue
        if not user_input.lower().endswith(".pdf"):
            print(f"❌ 请输入 PDF 文件：{user_input!r}\n")
            continue

        out_path = build_output_path(user_input)
        scale_pdf_content(user_input, out_path, SCALE)


if __name__ == "__main__":
    main()
