# coding=utf-8
# @Time    : 2026/8/5 15:15
# @Software: PyCharm
"""
PDF 页面提取工具 (PyMuPDF 版本)
通过输入 PDF 路径和页码范围，提取指定页面生成新的 PDF
"""

import fitz  # PyMuPDF
import os
import sys


def extract_pdf_pages(pdf_path: str, start_page: int, end_page: int, output_path: str = None) -> str:
    """
    从 PDF 中提取指定页码范围的页面
    
    Args:
        pdf_path: 原 PDF 文件路径
        start_page: 起始页码（从 1 开始）
        end_page: 结束页码（包含）
        output_path: 输出文件路径，默认在原文件同目录下生成
    
    Returns:
        生成的新 PDF 文件路径
    """
    # 验证文件存在
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"文件不存在: {pdf_path}")
    
    # 验证页码范围
    if start_page < 1:
        raise ValueError("起始页码不能小于 1")
    if end_page < start_page:
        raise ValueError("结束页码不能小于起始页码")
    
    # 打开 PDF 文档
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    
    if end_page > total_pages:
        doc.close()
        raise ValueError(f"结束页码 ({end_page}) 超过 PDF 总页数 ({total_pages})")
    
    # 生成输出文件名
    if output_path is None:
        directory = os.path.dirname(pdf_path)
        filename = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = os.path.join(directory, f"{filename}_页{start_page}-{end_page}.pdf")
    
    # 创建新文档并插入页面
    new_doc = fitz.open()
    
    # PyMuPDF 页码从 0 开始，所以需要 -1
    for page_num in range(start_page - 1, end_page):
        # 从原文档中复制页面到新文档
        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
    
    # 保存新 PDF
    new_doc.save(output_path, garbage=4, deflate=True)
    new_doc.close()
    doc.close()
    
    return output_path


def parse_page_range(page_range_str: str) -> tuple:
    """
    解析页码范围字符串
    
    支持格式:
        373-379  -> (373, 379)
        1        -> (1, 1)
    
    Args:
        page_range_str: 页码范围字符串，如 "373-379"
    
    Returns:
        (起始页, 结束页) 元组
    """
    page_range_str = page_range_str.strip()
    
    if '-' in page_range_str:
        parts = page_range_str.split('-')
        if len(parts) != 2:
            raise ValueError(f"页码范围格式错误: {page_range_str}")
        start = int(parts[0].strip())
        end = int(parts[1].strip())
        return start, end
    else:
        page = int(page_range_str)
        return page, page


def main():
    print("=" * 50)
    print("PDF 页面提取工具 (PyMuPDF)")
    print("=" * 50)
    
    # 输入 PDF 路径
    while True:
        pdf_path = input("\n请输入 PDF 文件路径: ").strip()
        if pdf_path:
            if os.path.exists(pdf_path):
                break
            else:
                print(f"文件不存在，请重新输入")
        else:
            print("路径不能为空")
    
    # 显示 PDF 信息
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        # 获取 PDF 元数据
        metadata = doc.metadata
        title = metadata.get('title', '未知')
        creator = metadata.get('creator', '未知')
        
        print(f"\nPDF 信息:")
        print(f"  总页数: {total_pages}")
        print(f"  标题: {title}")
        print(f"  创建工具: {creator}")
        doc.close()
    except Exception as e:
        print(f"读取 PDF 信息失败: {e}")
        total_pages = 0
    
    if total_pages == 0:
        print("无法读取 PDF 文件，程序退出")
        sys.exit(1)
    
    # 输入页码范围
    while True:
        page_range_input = input("\n请输入页码范围 (格式: 起始页-结束页，如 373-379): ").strip()
        if page_range_input:
            try:
                start_page, end_page = parse_page_range(page_range_input)
                print(f"  提取页码: {start_page} 到 {end_page}")
                
                # 验证页码范围
                if start_page > total_pages:
                    print(f"起始页码超过总页数 ({total_pages})，请重新输入")
                    continue
                if end_page > total_pages:
                    print(f"结束页码超过总页数 ({total_pages})，请重新输入")
                    continue
                if start_page < 1:
                    print("起始页码不能小于 1，请重新输入")
                    continue
                if end_page < start_page:
                    print("结束页码不能小于起始页码，请重新输入")
                    continue
                    
                break
            except ValueError as e:
                print(f"格式错误: {e}，请重新输入")
    
    # 选择输出路径
    output_dir = os.path.dirname(pdf_path)
    default_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    default_output = os.path.join(output_dir, f"{default_filename}_页{start_page}-{end_page}.pdf")
    
    output_input = input(f"\n输出文件路径 (直接回车使用默认路径):\n  {default_output}\n: ").strip()
    output_path = default_output if not output_input else output_input
    
    # 执行提取
    print("\n正在提取页面...")
    try:
        import time
        start_time = time.time()
        
        result_path = extract_pdf_pages(pdf_path, start_page, end_page, output_path)
        
        elapsed = time.time() - start_time
        print(f"\n✓ 提取成功!")
        print(f"  输出文件: {result_path}")
        print(f"  耗时: {elapsed:.3f} 秒")
        
        # 验证输出文件
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path)
            print(f"  文件大小: {file_size / 1024:.2f} KB")
    except Exception as e:
        print(f"\n✗ 提取失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
