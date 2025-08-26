# coding=utf-8
# @Time    : 2025/8/26 11:32
# @Software: PyCharm
from lxml import etree


def generate_xml_with_xsd():
    # 定义xsi命名空间URI
    xsi_ns = "http://www.w3.org/2001/XMLSchema-instance"
    ns_map = {
        'xsi': xsi_ns  # 注册xsi前缀
    }
    # 创建根元素时不直接设置命名空间属性
    root = etree.Element('tableList', nsmap=ns_map)
    # QName会自动处理命名空间与前缀的映射
    xsi_attr = etree.QName(xsi_ns, 'noNamespaceSchemaLocation')
    root.set(xsi_attr, '../../../ownWork/utils/xsds/fieldSQL.xsd')

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
