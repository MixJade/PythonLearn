# coding=utf-8
# @Time    : 2025/8/26 17:09
# @Software: PyCharm
from typing import NamedTuple
from lxml import etree


class FieldParam(NamedTuple):
    """field标签参数
    """
    code: str
    name: str
    length: str


def gen_field_xml(out_path: str, table_code: str, table_name: str, field_params: list[FieldParam]):
    """生成xml

    :param out_path: 输出路径
    :param table_code: 表的英文名
    :param table_name: 表的中文名
    :param field_params: 表下字段
    :return:
    """
    # 定义xsi命名空间URI
    xsi_ns = "http://www.w3.org/2001/XMLSchema-instance"
    ns_map = {
        'xsi': xsi_ns  # 注册xsi前缀
    }
    # 创建根元素时不直接设置命名空间属性
    root = etree.Element('tableList', nsmap=ns_map)
    # QName会自动处理命名空间与前缀的映射
    xsi_attr = etree.QName(xsi_ns, 'noNamespaceSchemaLocation')
    root.set(xsi_attr, '../../ownWork/utils/xsds/fieldSQL.xsd')

    # 创建子元素时设置属性
    table1 = etree.SubElement(root, 'table', code=table_code, name=table_name)

    for field_param in field_params:
        # 添加字段内容
        etree.SubElement(
            table1,
            'field',
            # 为子元素设置属性
            code=field_param.code,
            name=field_param.name,
            length=field_param.length
        )

    # 创建XML树并美化输出
    xml_tree = etree.ElementTree(root)
    xml_str = etree.tostring(xml_tree, pretty_print=True, encoding='UTF-8', xml_declaration=True)

    # 保存到文件
    with open(out_path, 'wb') as f:
        f.write(xml_str)

    print(f"XML文件生成成功: {out_path}")
