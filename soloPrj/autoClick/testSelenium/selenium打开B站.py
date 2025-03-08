import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

edge_driver_path = "../driver/msedgedriver.exe"  # 请替换为你的浏览器驱动路径
service = Service(edge_driver_path)
driver = webdriver.Edge(service=service)

# 窗口最大化
driver.maximize_window()

# 打开指定的 URL
driver.get("https://www.bilibili.com/")
time.sleep(5)  # 等待页面加载

# 输入搜索框(输入Hello World),find_element只获取一个元素
driver.find_element(By.CLASS_NAME, 'nav-search-input').send_keys("Hello World")

# 点击搜索(获取class属性的所有元素)
time.sleep(3)
driver.find_elements(By.CLASS_NAME, 'search-panel')[0].click()

# 最后退出
time.sleep(10)
driver.quit()
