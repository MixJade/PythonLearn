# coding=utf-8
# @Time    : 2024/5/25 16:46
# @Software: PyCharm
import json
import os
import time
import webbrowser

import pyautogui

# 先读取配置
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 打开一个默认的浏览器到url
webbrowser.open(config['myEdge']['url'])

# 确保最大化
time.sleep(1)
# (最大化)按下并释放Alt+空格组合键
pyautogui.hotkey('alt', 'space')
# 按下并释放'x'键
pyautogui.press('x')

# 点击打印按钮(目前是点击7次tab键即可)
time.sleep(1)
pyautogui.press('tab', presses=7, interval=0.1)
pyautogui.press(keys='enter')

# 等待弹出框
time.sleep(3)
pyautogui.press(keys='enter')  # 按下Enter
time.sleep(1)
# 设置文件名,并创建文件夹(保存到桌面)
filePath: str = f"%userprofile%\\Desktop\\{time.time() * 1000:.0f}"
os.makedirs(filePath)
fileName = config['fileName']['default']
pyautogui.write(f'{filePath}\\{fileName}', interval=0.05)
pyautogui.press(keys='enter', presses=2, interval=0.5)  # 按下Enter(确保当前输入法是中文)

# 最后关闭浏览器
pyautogui.hotkey('ctrl', 'shift', 'w')
# 使用os模块的startfile方法打开文件夹
os.startfile(filePath)
