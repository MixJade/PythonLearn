# coding=utf-8
# @Time    : 2025/7/21 10:54
# @Software: PyCharm
import openpyxl


def read_excel_columns(file_path):
    """
    读取Excel文件中除第一个工作表外的所有工作表的第二、三列数据（从第二行开始）

    参数:
    file_path (str): Excel文件路径

    返回:
    dict: 以表名为键，每行的第二、三列数据为值的字典
    """
    try:
        # 加载工作簿
        workbook = openpyxl.load_workbook(file_path, read_only=True)

        # 获取除第一个工作表外的所有工作表
        sheets = workbook.worksheets[1:]

        # 存储结果的字典
        results = {}

        # 遍历每个工作表
        for sheet in sheets:
            sheet_data = []
            # 从第二行开始遍历（min_row=2）
            for row in sheet.iter_rows(min_row=2, values_only=True):
                # 获取第二、三、四列的值（索引1、2、3）
                col_b, col_c, col_d = row[1], row[2], row[3]
                if col_b is not None:
                    sheet_data.append((col_b, col_c, col_d))

            # 将该工作表的数据添加到结果字典中
            results[sheet.title] = sheet_data

        # 关闭工作簿
        workbook.close()

        return results

    except Exception as e:
        print(f"处理文件时出错: {e}")
        return {}


def print_results(results):
    """
    按工作表打印结果

    参数:
    results (dict): 以表名为键，每行的第二、三列数据为值的字典
    """
    for sheet_name, data in results.items():
        print(f"\ninterface {sheet_name} {{")
        for row in data:
            col_b, col_c, col_d = row
            # 特殊判定
            if col_c == "Integer":
                col_c = "number"
            elif col_c == "String":
                col_c = "string"
            print(f"    {col_b}: {col_c}; // {col_d}")
        print("}")


if __name__ == "__main__":
    file_path = r"your_excel_file.xlsx"  # 替换为实际文件路径
    results = read_excel_columns(file_path)
    print_results(results)
