# coding=utf-8
# @Time    : 2025/10/15 15:33
# @Software: PyCharm
from docx import Document


def read_target_tables(word_path):
    # 目标表头（注意分隔符是制表符\t，需与Word表格一致）
    target_header = "是否必填"

    # 加载Word文档
    doc = Document(word_path)

    # 遍历文档中的所有表格
    for table_idx, table in enumerate(doc.tables, 1):
        # 提取表格第一行（表头）
        header_cells = [cell.text.strip() for cell in table.rows[0].cells]

        # 检查表头是否包含目标表头
        if target_header in header_cells:
            print(f"\n===== 找到匹配表格（表格序号：{table_idx}） =====")
            # 找到"是否必填"所在的列索引
            required_col_idx = header_cells.index(target_header)
            # 遍历表格的每一行并输出
            for row_idx, row in enumerate(table.rows, 1):
                row_data = [cell.text.strip() for cell in row.cells]
                # 检查"是否必填"列的值是否为"条件必填"（可根据实际文本调整判断条件）
                if row_data[required_col_idx] == "条件必填":
                    print(f"行 {row_idx}: {row_data}")


# 示例用法
if __name__ == "__main__":
    # 替换为你的Word文件路径
    word_file_path = r"your_file.docx"
    read_target_tables(word_file_path)
