# coding=utf-8
# @Time    : 2026/4/15
# @Software: PyCharm
import os
import fitz  # pymupdf

"""
PDF发票2合1 —— 将两张发票拼为一张A4（上下排列）
"""

# ── A4 尺寸（单位：pt，72pt = 1 inch）
A4_W = 595.0
A4_H = 842.0


def draw_divider(page: fitz.Page, y: float, width: float = A4_W,
                 color=(0, 1, 0), line_width: float = 1.0):
    """在页面 y 坐标处画一条贯穿全宽的绿色横线。"""
    page.draw_line(
        fitz.Point(0, y),
        fitz.Point(width, y),
        color=color,
        width=line_width,
    )


def merge_2in1_a4(pdf_paths: list[str], output_path: str):
    """将 1 或 2 个 PDF 的第一页拼合为一张 A4（上下各占一半）。
    - 2 个文件：上半放 pdf_paths[0]，下半放 pdf_paths[1]
    - 1 个文件：上半放该文件，下半留空白
    每张发票底部（即区域下边缘）绘制一条绿色横线。
    """
    half_h = A4_H / 2  # ≈ 421 pt

    # 新建一张空白 A4 文档
    out_doc = fitz.open()
    out_page = out_doc.new_page(width=A4_W, height=A4_H)

    for idx, pdf_path in enumerate(pdf_paths[:2]):
        src_doc = fitz.open(pdf_path)

        # 目标区域：idx=0 → 上半，idx=1 → 下半
        if idx == 0:
            target_rect = fitz.Rect(0, 0, A4_W, half_h)
        else:
            target_rect = fitz.Rect(0, half_h, A4_W, A4_H)

        # show_pdf_page 会自动缩放并保持宽高比居中
        out_page.show_pdf_page(target_rect, src_doc, 0, keep_proportion=True, overlay=True)
        src_doc.close()

        # 在该发票底部画绿色横线
        bottom_y = half_h if idx == 0 else A4_H
        draw_divider(out_page, bottom_y)

    # 若只有一张发票，也在中间分隔线处补一条横线（视觉上区分上下区域）
    if len(pdf_paths) == 1:
        draw_divider(out_page, half_h)

    out_doc.save(output_path, garbage=4, deflate=True)
    out_doc.close()
    print(f"✅ 合成完成：{output_path}\n")


def build_output_path(paths: list[str]) -> str:
    """根据输入文件名生成输出文件名，保存在第一个文件的同目录下。"""
    base_names = [os.path.splitext(os.path.basename(p))[0] for p in paths]
    out_name = "merger_" + "_".join(base_names) + ".pdf"
    out_dir = os.path.dirname(os.path.abspath(paths[0]))
    return os.path.join(out_dir, out_name)


def main():
    print("=" * 55)
    print("   PDF 发票 2合1 合成工具（A4 上下排版）")
    print("=" * 55)
    print("使用说明：")
    print("  · 每次输入一个 PDF 路径，可直接拖入文件")
    print("  · 输入 2 个后自动合成")
    print("  · 只有 1 个时输入 1 强制合成（下半留空）")
    print("  · 输入 0 退出程序\n")
    pending: list[str] = []  # 待合成队列

    while True:
        prompt = f"请输入 PDF 路径（当前 {len(pending)}/2，0=退出，1=强制合成）：\n> "
        raw = input(prompt).strip()
        # ── 去掉拖入文件时系统自动添加的引号
        user_input = raw.strip('"').strip("'")
        if user_input == "0":
            if pending:
                print(f"⚠️  还有 {len(pending)} 个文件未合成，已放弃。")
            print("👋 退出程序")
            break

        # ── 强制合成单个文件
        if user_input == "1":
            if len(pending) == 1:
                out_path = build_output_path(pending)
                merge_2in1_a4(pending, out_path)
                pending.clear()
            else:
                print("❌ 当前没有待处理的文件，或已有 2 个文件（无需强制）\n")
            continue
        # ── 验证文件
        if not os.path.isfile(user_input):
            print(f"❌ 文件不存在，请重新输入：{user_input!r}\n")
            continue
        if not user_input.lower().endswith(".pdf"):
            print(f"❌ 请输入 PDF 文件，当前文件后缀不是 .pdf：{user_input!r}\n")
            continue
        pending.append(user_input)
        print(f"📥 已接收（{len(pending)}/2）：{os.path.basename(user_input)}")
        # ── 凑满 2 个自动合成
        if len(pending) == 2:
            out_path = build_output_path(pending)
            merge_2in1_a4(pending, out_path)
            pending.clear()


if __name__ == "__main__":
    main()
