# coding=utf-8
# @Time    : 2024/5/25 16:34
# @Software: PyCharm
from datetime import datetime

import pyautogui

# 获取屏幕分辨率
screenWidth, screenHeight = pyautogui.size()
print(f"当前屏幕分辨率：{screenWidth}x{screenHeight}")
# 获取当前时间
now = datetime.now()
# 格式化时间
formatted_time = f"{now.year}年{now.month}月{now.day}日{now.hour}时"
print(f"当前时间：{formatted_time}")
