# coding=utf-8
# @Time    : 2026/4/4 15:21
# @Software: PyCharm
import os
import zipfile


def txt_to_zip(txt_file_path, zip_file_name=None):
    """将单个txt文件压缩为zip格式

    :param txt_file_path: 你的txt文件路径（如 "test.txt"）
    :param zip_file_name: 输出的zip文件名（不填则自动用txt文件名+.zip）
    """
    # 如果没指定zip文件名，自动生成
    if zip_file_name is None:
        zip_file_name = os.path.splitext(txt_file_path)[0] + ".zip"

    # 创建zip文件并压缩
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(txt_file_path, os.path.basename(txt_file_path))

    print(f"✅ 压缩完成！文件已保存为：{zip_file_name}")


# 把这里改成你的txt文件名/路径
txt_to_zip("../outputFile/zip炸弹文件.txt")
