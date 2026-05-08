# coding=utf-8
# @Time    : 2024/6/11 21:57
# @Software: PyCharm
import os
import subprocess

"""
pandoc转化md为epub

以及对md进行预处理：
    1. 加元数据标题
    2. 每行前加特殊空格
"""


def preprocess_md(input_md: str) -> None:
    """对md文件进行预处理：添加元数据标题 + 超长行缩进"""
    md_name = os.path.splitext(os.path.basename(input_md))[0]

    with open(input_md, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.splitlines(keepends=True)

    # 1. 头部加入元数据标题（已是 --- 开头则跳过）
    if not content.lstrip().startswith("---"):
        header = f"---\ntitle: 《{md_name}》\nlanguage: zh-CN\n---\n\n"
        lines.insert(0, header)

    # 2. 超过60字符的行前加入全角空格缩进（已是空格/全角空格开头则跳过）
    processed = []
    for line in lines:
        stripped = line.rstrip("\n\r")
        if (
                len(stripped) > 60
                and stripped != ""
                and not stripped[0].isspace()
                and not stripped.startswith("　")
        ):
            line = "　　" + line.lstrip(" ")
        processed.append(line)

    with open(input_md, "w", encoding="utf-8") as f:
        f.writelines(processed)

    print(f"预处理完成：{input_md}")


def turn_md_epub(input_md: str) -> None:
    if input_md.endswith(".md"):
        # 询问是否预处理
        choice = input("是否对md文件进行预处理？（注意：会直接修改原md文件）[1是/0否]: ").strip()
        if choice == "1":
            preprocess_md(input_md)

        print("开始转换epub")
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
