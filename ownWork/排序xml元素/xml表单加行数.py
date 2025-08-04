# coding=utf-8
# @Time    : 2025/8/4 14:35
# @Software: PyCharm
from lxml import etree

parser = etree.XMLParser(remove_blank_text=True)  # 保留空白格式
tree = etree.parse('样例表单_排序后.xml', parser)
root = tree.getroot()
# 获取所有 formelement 元素
form_elements = root.findall('formelement')


def add_one_line(match_label: str):
    """
    通过labelname来匹配行，其后续元素的行数都+1
    目前只支持添加1整行
    """
    is_match = False  # 是否匹配上
    for element in form_elements:
        # 已经匹配上，则之后行的row+1
        if is_match:
            element.set('row', str(int(element.get('row')) + 1))
        # 匹配到行以后,其后续元素的row+1
        if element.get('labelname') == match_label:
            is_match = True


if __name__ == '__main__':
    # 需要在其之后增加行数，所在行的labelname
    add_one_line('二号2')
    add_one_line('三号2')
    # 保存修改后的 XML 文件（使用lxml的序列化功能）
    tree.write('样例表单添加行_结果.xml',
               encoding='UTF-8',
               xml_declaration=True,
               pretty_print=True)  # 添加漂亮打印格式
    print("行数增加完成，结果已保存到 样例表单添加行_结果.xml")
