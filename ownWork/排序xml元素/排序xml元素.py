# coding=utf-8
# @Time    : 2025/6/5 11:07
# @Software: PyCharm
from lxml import etree

# 解析 XML 文件（使用lxml的解析器）
parser = etree.XMLParser(remove_blank_text=True)  # 保留空白格式
tree = etree.parse('样例表单.xml', parser)
root = tree.getroot()

# 获取所有 formelement 元素
form_elements = root.findall('formelement')

# 按照 row 属性排序
form_elements.sort(key=lambda el: int(el.get('row')))

# 移除所有现有元素（准备重新添加排序后的元素）
for element in form_elements:
    root.remove(element)

# 按行分组，排除 fieldtype="99" 的元素
row_groups = {}
for element in form_elements:
    if element.get('fieldtype') != '99':
        row = element.get('row')
        if row not in row_groups:
            row_groups[row] = []
        row_groups[row].append(element)

# 处理每组的第一个元素
for row, group in row_groups.items():
    if group:
        if len(group) == 1:
            first_element = group[0]
            first_element.set('labelcol', '1')
            first_element.set('fieldcol', '2')
        elif len(group) == 2:
            first_element = group[0]
            first_element.set('labelcol', '1')
            first_element.set('fieldcol', '2')
            first_element_2 = group[1]
            first_element_2.set('labelcol', '3')
            first_element_2.set('fieldcol', '4')
        else:
            print(f"存在异常行： {row=} {len(row)=}")

# 重新生成 formactiveid 并重新添加元素到树中
for index, element in enumerate(form_elements, start=1):
    element.set('formactiveid', str(index))
    root.append(element)  # 将排序后的元素添加回根节点

# 保存修改后的 XML 文件（使用lxml的序列化功能）
tree.write('样例表单_排序后.xml',
           encoding='UTF-8',
           xml_declaration=True,
           pretty_print=True)  # 添加漂亮打印格式

print("排序和重新编号完成，结果已保存到 样例表单_排序后.xml")
