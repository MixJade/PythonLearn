# coding=utf-8
# @Time    : 2025/7/3 17:11
# @Software: PyCharm
import fitz  # PyMuPDF

"""
上述依赖如此下载：pip install pymupdf
"""


def delete_pages(input_pdf, output_pdf, pages_to_delete):
    """
    删除 PDF 中指定的页码

    参数:
    input_pdf (str): 输入 PDF 文件路径
    output_pdf (str): 输出 PDF 文件路径
    pages_to_delete (list): 要删除的页码列表（从 1 开始）
    """
    # 打开 PDF 文件
    doc = fitz.open(input_pdf)

    # 转换为基于 0 的索引（PyMuPDF 使用 0 开始的页码）
    pages_to_delete_0based = [page - 1 for page in pages_to_delete]

    # 从后往前删除，避免索引变化
    for page_num in sorted(pages_to_delete_0based, reverse=True):
        if 0 <= page_num < len(doc):
            doc.delete_page(page_num)

    # 优化文件结构并压缩
    doc.save(output_pdf, garbage=4, deflate=True)
    # 保存修改后的 PDF
    # doc.save(output_pdf)
    doc.close()

    print(f"已成功删除指定页面，新文件保存在: {output_pdf}")


# 使用示例
input_file = r"input.pdf"  # 替换为你的输入 PDF 路径
output_file = "output.pdf"  # 替换为你的输出 PDF 路径
pages_to_del = []  # 要删除的页码列表（例如删除第 1、3、5 页）

# 比如删除1-360页
for i in range(1, 361):
    pages_to_del.append(i)

delete_pages(input_file, output_file, pages_to_del)
