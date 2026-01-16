# coding=utf-8
# @Time    : 2026-01-16 17:39
# @Software: PyCharm
from lxml import etree


"""开始处理新版的字段
"""
input_xml = r"按钮权限与菜单关系.xml"
with open(input_xml, 'rb') as xml_file:
    xml_tree = etree.parse(xml_file)
root = xml_tree.getroot()
for table in root.xpath('//menu'):
    # 遍历当前表字段
    sa = 0
    stsaa = ''
    for field in table.xpath('./btn'):
        # 没有匹配上
        stsaa += f"'{field.get('code')}',"
        sa += 1
    stsaa = stsaa[0:-1]
    # noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
    print(f"""
-- 查看 {table.get('name')} 按钮权限 预计{sa}条
SELECT *
FROM sys_menus_info
where MENUS_NO IN ({stsaa});

-- 更正 {table.get('name')} 按钮权限
update sys_menus_info
set USE_STATE    = '1',
    PARN_NODE_ID = '{table.get('code')}'
where MENUS_NO IN ({stsaa});
""")


