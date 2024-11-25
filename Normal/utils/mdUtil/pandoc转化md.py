# coding=utf-8
# @Time    : 2024/6/11 21:57
# @Software: PyCharm
import os
import subprocess


def turn_md_epub(input_md: str) -> None:
    if input_md.endswith(".md"):
        output_epub = input_md[:-len("md")] + "epub"
        command = [
            'pandoc',
            input_md,
            '-o', output_epub,
        ]

        subprocess.run(command, check=True)
        print("文件输出至:" + output_epub)
    else:
        print("请输入md格式的文件")
        return


if __name__ == '__main__':
    print("(输入1可选同文件夹全部md文件)")
    input_md1 = input("请输入md文件路径:")
    if input_md1 == '1':
        file_path = input("输入某个md文件路径:")
        # 获取文件路径
        directory = os.path.dirname(file_path)
        # 获取文件夹中所有的文件（只读取文件，不读取文件夹）
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(".md")]
        print("存在的md文件：", files)
        for item in files:
            turn_md_epub(os.path.join(directory, item))
    else:
        turn_md_epub(input_md1)
