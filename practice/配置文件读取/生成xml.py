# coding=utf-8
# @Time    : 2025/8/26 11:32
# @Software: PyCharm
from lxml import etree


def generate_xml_with_xsd():
    # 定义命名空间
    ns = {
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'noNamespaceSchemaLocation': '../../../ownWork/utils/xsds/fieldSQL.xsd'  # 自定义命名空间
    }

    # 创建根元素，并指定XSD引用
    root = etree.Element(
        'tableList',  # 带命名空间的根元素
        nsmap=ns,  # 注册命名空间
    )

    # 创建子元素时设置属性
    table1 = etree.SubElement(
        root,
        'table',
        # 为子元素设置属性
        code="STUDENT_INF",
        name="学生表"
    )
    # 为子元素添加内容
    etree.SubElement(
        table1,
        'field',
        # 为子元素设置属性
        code="stu_name",
        name="学生名称",
        length="VARCHAR2(16)"
    )

    # 创建XML树并美化输出
    xml_tree = etree.ElementTree(root)
    xml_str = etree.tostring(xml_tree, pretty_print=True, encoding='UTF-8', xml_declaration=True)

    # 保存到文件
    with open('testRead/生成xml_结果.xml', 'wb') as f:
        f.write(xml_str)

    print("XML文件生成成功，已引用XSD schema")


if __name__ == "__main__":
    generate_xml_with_xsd()
