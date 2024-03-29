# coding=utf-8
# @Time    : 2024/3/28 11:21
# @Software: PyCharm
import subprocess


def set_clipboard_text(text):
    """通过调用Window的clip工具来插入剪贴板,不通用

    :param text: 待复制文本
    """
    process = subprocess.Popen('clip', stdin=subprocess.PIPE, close_fds=True)
    process.communicate(input=text.encode())


set_clipboard_text('Hello, world!')
