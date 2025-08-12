# coding=utf-8
# @Time    : 2025/8/12 9:43
# @Software: PyCharm
from lxml import etree

# 解析 XML 文件（使用lxml的解析器）
parser = etree.XMLParser(remove_blank_text=True)  # 保留空白格式
tree = etree.parse(r'tesXml/2样例table.xml', parser)
root = tree.getroot()

table_item = root.findall('tableitem')

begin_id = 1
begin_index = 0
# 重设id、index
for element in table_item:
    element.set('id', str(begin_id))
    element.set('indexed', str(begin_index))
    begin_id += 1
    begin_index += 1

# 保存修改后的 XML 文件（使用lxml的序列化功能）
tree.write('tesXml/6样例table_结果.xml',
           encoding='UTF-8',
           xml_declaration=True,
           pretty_print=True)  # 添加漂亮打印格式

print("排序和重新编号完成，结果已保存到 tesXml/6样例table_结果.xml")
