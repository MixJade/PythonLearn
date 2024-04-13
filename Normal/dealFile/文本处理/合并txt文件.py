# coding=utf-8
# @Time    : 2024/4/13 16:15
# @Software: PyCharm
import os

# 搜索的文件夹路径
folder_path = r"../../outputFile/章节拆分/"

# 最终结果的文件
output_file = "../../outputFile/合并txt文件.md"

# 遍历文件夹中所有txt文件
with open(output_file, 'w', encoding='utf-8') as outfile:
    for filename in os.listdir(folder_path):
        # 检查文件是否为.txt文件
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as readfile:
                # 写入文件标题（即文件名）
                outfile.write("# " + filename.replace('.txt', '') + "\n\n")
                # 写入文件内容
                outfile.write(readfile.read())
                # 在文件间添加一个空行
                outfile.write("\n")
