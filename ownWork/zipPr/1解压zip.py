# coding=utf-8
# @Time    : 2025/11/25 14:11
# @Software: PyCharm
import zipfile


def unzip_file(zip_path):
    if zip_path.endswith(".zip"):
        extract_path = zip_path[0:-4]  # 新建一个同名文件夹
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(extract_path)  # 解压所有文件到指定路径
            print(f"解压完成！文件保存至：{extract_path}")


# 调用
unzip_file("测试压缩文件夹_结果.zip")
