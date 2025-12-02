# coding=utf-8
# @Time    : 2025/12/2 17:39
# @Software: PyCharm
import shutil

"""
不建议使用这个，最好还是使用360压缩
"""
# 待压缩的文件夹路径
source_folder = r"测试压缩文件夹"
# 生成的ZIP文件路径（base_name="output" → 生成output.zip）
zip_base_name = "output_结果"

# 执行压缩（format="zip" 指定为ZIP格式）
shutil.make_archive(zip_base_name, "zip", root_dir=source_folder)

print(f"压缩完成！ZIP文件路径：{zip_base_name}.zip")
