# coding=utf-8
# @Time    : 2025/7/19 13:29
# @Software: PyCharm
import os
from pathlib import Path

import pandas as pd


def merge_csv_to_excel(csv_folder, output_file):
    # 创建Excel写入对象
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # 遍历文件夹中的所有CSV文件
        for csv_file in Path(csv_folder).glob('*.csv'):
            # 获取CSV文件名（不含扩展名）作为sheet名
            sheet_name = csv_file.stem[:31]  # Excel sheet名最大长度为31个字符

            try:
                # 读取CSV文件
                df = pd.read_csv(csv_file)

                # 将数据写入Excel的对应sheet
                df.to_excel(writer, sheet_name=sheet_name, index=False)

                print(f"成功将 {csv_file.name} 写入sheet: {sheet_name}")
            except Exception as e:
                print(f"处理文件 {csv_file.name} 时出错: {str(e)}")


if __name__ == "__main__":
    # 配置参数
    input_csv_folder = input("请输入CSV文件所在文件夹路径: ")
    input_output_file = input("请输入输出Excel文件路径（例如 output.xlsx）: ")

    # 检查文件夹是否存在
    if not os.path.exists(input_csv_folder):
        print(f"错误: 文件夹 {input_csv_folder} 不存在")
    else:
        merge_csv_to_excel(input_csv_folder, input_output_file)
        print(f"\n合并完成，输出文件: {input_output_file}")
