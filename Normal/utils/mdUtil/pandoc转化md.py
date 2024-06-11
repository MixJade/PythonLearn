# coding=utf-8
# @Time    : 2024/6/11 21:57
# @Software: PyCharm
import subprocess


def turn_md_epub() -> None:
    input_md = input("请输入md文件路径:")
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
    turn_md_epub()
