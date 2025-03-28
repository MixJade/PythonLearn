# coding=utf-8
# @Time    : 2024-12-05 09:57:58
# @Software: PyCharm

"""给md小说，每段的前面加四个空格
"""

# 构建文件路径(桌面上的文件)
file_name = input("请输入md文件路径(可直接拖入终端):").strip('"')
"""一、正文处理
"""
results = []

# 读取文件
with open(file_name, "r", encoding='utf-8') as f:
    # last_line_was_blank = True  # 用一个标志位记录上一行是否为空行
    for line in f:
        # 给正文的每一行前面加上空格
        if not (line.startswith('---')
                or line.startswith('#')
                or line == '\n'
                or line.startswith('title')
                or line.startswith('language')):
            line = "　　" + line
        # 如果当前行不为空且上一行也不为空，那么在当前行前插入一个空行
        # if line.strip() != '' and not last_line_was_blank:
        #     results.append("\n")
        # 更新标志位
        # last_line_was_blank = line.strip() == ''
        results.append(line)

"""二、输出文件
"""
# 将替换后的内容写回文件
with open(file_name, 'w', encoding='utf-8') as file:
    for line in results:
        file.write(line)

print("文件已经输出至：" + file_name)
print("请检查文件的开头，防止可能存在异常情况")
