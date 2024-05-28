# coding=utf-8
# @Time    : 2024/5/25 16:46
# @Software: PyCharm
import json
import os
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

# 保存路径
save_path: str = os.path.join(os.getcwd(), f"{time.time() * 1000:.0f}")
os.makedirs(save_path)

# 浏览器设置
settings = {
    "recentDestinations": [{
        "id": "Save as PDF",
        "origin": "local",
        "account": ""
    }],
    "selectedDestinationId": "Save as PDF",
    "version": 2,  # 另存为pdf，1 是默认打印机
    "isHeaderFooterEnabled": False,  # 是否勾选页眉和页脚
    "isCssBackgroundEnabled": True,  # 是否勾选背景图形
    "mediaSize": {
        "height_microns": 297000,
        "name": "ISO_A4",
        "width_microns": 210000,
        "custom_display_name": "A4",
    },
}
prefs = {
    'printing.print_preview_sticky_settings.appState': json.dumps(settings),
    'savefile.default_directory': save_path,
}
options = Options()
options.add_experimental_option("prefs", prefs)

# 使用 --kiosk-printing 来启用 "silent printing"
options.add_argument("--kiosk-printing")

# 请确保 chrome_driver_path 指向正确的 ChromeDriver 位置
chrome_driver_path = "../driver/chromedriver.exe"  # 请替换为你的 ChromeDriver 路径
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# 打开指定的 URL
driver.get("https://print.yingyutifen.cn/print/pc.html?aptmId=3229520")

# 等待页面加载(当wordList这个类加载出来再开始行动,最多等30s)
WebDriverWait(driver, timeout=30).until(
    ec.presence_of_element_located((By.CLASS_NAME, "wordList"))
)

# 打印阅读
file_name1 = "测试打印阅读"
driver.execute_script(f"document.title = '{file_name1}';")
driver.execute_script("window.print();")

# 打印单词中文
btn_text = "打印中文"
file_name2 = f"测试{btn_text}"
try:
    # 动态构建XPath表达式并查找元素
    element = driver.find_element(By.XPATH, f"//button[contains(text(), '{btn_text}')]")
    element.click()
    # 在这里可以对找到的元素执行操作，比如点击
    driver.execute_script(f"document.title = '{file_name2}';")
    driver.execute_script("window.print();")
except NoSuchElementException as e:
    print(f"未找到元素：'{btn_text}', 错误信息：{e}")

# 使用os模块的startfile方法打开文件夹
os.startfile(save_path)
