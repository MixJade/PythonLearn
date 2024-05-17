# coding=utf-8
# @Time    : 2024/5/17 14:00
# @Software: PyCharm
import hashlib
import time
from tkinter import *

LOG_LINE_NUM = 0


def get_current_time():
    """获取当前时间
    """
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return current_time


class MyGUI:
    def __init__(self, init_window_name):
        self.str_trans_to_md5_button = None
        self.log_data_Text = None
        self.result_data_Text = None
        self.init_data_Text = None
        self.log_label = None
        self.result_data_label = None
        self.init_data_label = None
        self.init_window_name = init_window_name

    def set_init_window(self):
        """设置窗口"""
        self.init_window_name.title("文本处理工具_v1.2")  # 窗口名
        self.init_window_name.geometry('1068x481+10+10')  # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name["bg"] = "green"  # 窗口背景色
        # 标签
        self.init_data_label = Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)
        # 文本框
        self.init_data_Text = Text(self.init_window_name, width=67, height=18)  # 原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=24)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        # 按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="字符串转MD5", bg="lightblue", width=10,
                                              command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=1, column=11)

    # 功能函数
    def str_trans_to_md5(self):
        src = self.init_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        if src:
            my_md5 = hashlib.md5()
            my_md5.update(src)
            my_md5_digest = my_md5.hexdigest()
            # 输出到界面
            self.result_data_Text.delete(1.0, END)
            self.result_data_Text.insert(1.0, my_md5_digest)
            self.write_log_to_text("INFO:str_trans_to_md5 success")
        else:
            self.write_log_to_text("ERROR:str_trans_to_md5 failed")

    def write_log_to_text(self, log_msg):
        """日志动态打印"""
        global LOG_LINE_NUM
        current_time = get_current_time()
        log_msg_in = str(current_time) + " " + str(log_msg) + "\n"  # 换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, log_msg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, log_msg_in)


if __name__ == '__main__':
    init_window = Tk()  # 实例化出一个父窗口
    zmj_portal = MyGUI(init_window)
    # 设置根窗口默认属性
    zmj_portal.set_init_window()
    # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
    init_window.mainloop()
