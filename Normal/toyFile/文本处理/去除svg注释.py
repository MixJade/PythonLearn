# coding=utf-8
# @Time    : 2024/3/28 11:24
# @Software: PyCharm
import subprocess

svg_path: str = input("请输入需要去除注释的svg路径:")
# svg_path: str = r"C:\MyCode\测试流程示意图.svg"
res_text_list: list[str] = []

# 去除有注释的行
with open(svg_path, 'r', encoding='utf-8') as f:
    # 遍历每一行
    for line in f:
        # 检查如果行中没有"<!-- xxx-->"格式的字符串
        if '<!--' not in line and '-->' not in line:
            # 打印行
            res_text_list.append(line)
res_text: str = "".join(res_text_list)

# 将去除注释的结果放入剪贴板
process = subprocess.Popen('clip', stdin=subprocess.PIPE, close_fds=True)
process.communicate(input=res_text.encode())
print("去除注释后的svg已复制到剪贴板")
