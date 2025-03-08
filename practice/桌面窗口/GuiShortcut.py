# coding=utf-8
# @Time    : 2024/5/25 21:50
# @Software: PyCharm
import os
import tkinter as tk
from functools import partial


class MyDirBtn:
    # (当前文件的上二级目录)等价于r"C:\MyCode"
    code_dir = os.path.abspath(os.path.join(os.getcwd(), "../../.."))

    def __init__(self, name: str, path: str, bg_color: str) -> None:
        self.name = name  # 按钮名称
        self.path = self.code_dir + path  # 文件夹路径
        self.bgColor = bg_color  # 背景颜色


# 设置链接配置
myBtn: list = [
    MyDirBtn(name="Python脚本", path=r"\PythonLearn\Normal\utils\pyCmd", bg_color="#89e051"),
    MyDirBtn(name="Python笔记", path=r"\PythonLearn\docs", bg_color="#00FF00"),
    MyDirBtn(name="前端笔记", path=r"\TsLearn\docs", bg_color="#13cff4"),
    MyDirBtn(name="Java笔记", path=r"\JavaLearn\docs\2023", bg_color="#ff226d"),
    MyDirBtn(name="图片文件", path=r"\MyPicture\public", bg_color="#ffffff"),
    MyDirBtn(name="图片服务", path=r"\MyPicture\script", bg_color="#5F9EA0"),
]


def jump_dir(dir_path: str):
    """跳转到特定目录
    """
    try:
        os.startfile(dir_path)
    except FileNotFoundError:
        print(f"不存在的目录：{dir_path}")


# 设置主界面
root = tk.Tk()
root.geometry('300x240')
root.title("我的快捷方式")

# 循环放入按钮
for item in myBtn:
    # 使用functools设置传参,第一个参数是函数，第二个是传参
    my_func_with_arg = partial(jump_dir, item.path)
    # 放入按钮
    tk.Button(root, text=item.name, command=my_func_with_arg, width=28, background=item.bgColor).pack()

# 让界面等待
root.mainloop()
