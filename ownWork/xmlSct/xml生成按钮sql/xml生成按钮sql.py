# coding=utf-8
# @Time    : 2025/9/12 16:12
# @Software: PyCharm
from lxml import etree

from utils.outBtnRoleSQL import *

# 解析 XML 文件（使用lxml的解析器）
# 读取并解析XML
with open("按钮及权限.xml", 'rb') as xml_file:
    xml_tree = etree.parse(xml_file)
root = xml_tree.getroot()

# 遍历每个分组并填入
menu_list: list[Menu] = []
# 遍历所有字典
for menu1 in root.xpath('//menu'):
    menu_no = menu1.get('menuNo')
    menu_desc = menu1.get('desc')
    # 读取菜单下的按钮列表
    menu_btn_list: list[Btn] = []
    for btn1 in menu1.xpath('./btn'):
        btn_role_list: list[Role] = []
        for role1 in btn1.xpath('./role'):
            btn_role_list.append(Role(role1.get('roleNo'), role1.get('roleName')))
        menu_btn_list.append(Btn(btn1.get('btnName'), btn_role_list))
    menu_list.append(Menu(menu_no, menu_desc, menu_btn_list))

# 探查
print("\n-- " + "=" * 50)
for menu in menu_list:
    out_hy_menu_btn_sql(menu, is_hy=False)
# 插入数据
print("\n-- " + "=" * 50)
for menu in menu_list:
    out_insert_menu_btn_sql(menu)
# 核验
print("\n-- " + "=" * 50)
for menu in menu_list:
    out_hy_menu_btn_sql(menu)
