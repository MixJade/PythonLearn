# coding=utf-8
# @Time    : 2025/8/4 14:35
# @Software: PyCharm
from lxml import etree

parser = etree.XMLParser(remove_blank_text=True)  # 保留空白格式
tree = etree.parse('样例表单_排序后.xml', parser)
root = tree.getroot()

# 获取所有 formelement 元素
form_elements = root.findall('formelement')

"""
通过labelname来匹配行，其后续元素的行数都+1
目前只支持添加1整行
"""
# 需要在其之后增加行数，所在行的labelname
new_line_label = ['二号2', '三号3']

# 添加的行数(初始值，勿动)
add_num = 0
# 遍历所有元素
for element in form_elements:
    element.set('row', str(int(element.get('row')) + add_num))
    # 匹配到行以后,其后续元素的row+1
    if element.get('labelname') in new_line_label:
        add_num += 1

# 保存修改后的 XML 文件（使用lxml的序列化功能）
tree.write('样例表单添加行_结果.xml',
           encoding='UTF-8',
           xml_declaration=True,
           pretty_print=True)  # 添加漂亮打印格式

print("行数增加完成，结果已保存到 样例表单添加行_结果.xml")
