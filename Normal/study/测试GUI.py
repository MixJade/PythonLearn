# coding=utf-8
# @Time    : 2024/5/17 14:00
# @Software: PyCharm
import tkinter as tk

# 这个示例程序创建了一个简单的窗口，并在窗口中添加了一个标签，显示“Hello, World!”
# 导入Tkinter模块

# 创建一个主窗口
root = tk.Tk()
# 设置窗口标题
root.title("Hello, Tkinter!")

# 创建一个标签，并设置其文本内容为"Hello, World!"
label = tk.Label(root, text="Hello, World!")
# 将标签添加到窗口中
label.pack()

# 创建按钮
button = tk.Button(root, text='Click me!', command=root.quit)
button.pack()

# 运行主循环，等待用户交互
root.mainloop()
