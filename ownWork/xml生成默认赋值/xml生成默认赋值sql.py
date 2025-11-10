# coding=utf-8
# @Time    : 2025/8/6 14:32
# @Software: PyCharm
from lxml import etree
from typing import NamedTuple

from utils.convertCase import camel_to_snake, out_spilt_line

with open(r"各字段默认赋值逻辑.xml", 'rb') as xml_file:
    xml_tree = etree.parse(xml_file)
root = xml_tree.getroot()


class CheckDo(NamedTuple):
    """字段赋值参数
    """
    type: str  # 用于区分筛选条件的类型，0为无条件默认
    desc: str  # 条件的中文注释
    con_1: str  # 筛选条件1
    con_2: str  # 筛选条件2
    con_3: str  # 筛选条件3
    value: str  # 最终赋值


class FieldDo(NamedTuple):
    """字段
    """
    java_name: str  # 实体类中字段名称,形如:prjName
    desc: str  # 字段注释,形如:项目名称
    sql_field: str  # SQL字段名称,形如:PRJ_NAME
    check_list: list[CheckDo]  # 各种条件下字段的赋值


# 遍历所有字段配置
field_list: list[FieldDo] = []
for field in root.xpath('//field'):
    check_list: list[CheckDo] = []
    code_ = field.get('code')
    field_list.append(
        FieldDo(java_name=code_, desc=field.get('desc'), sql_field=camel_to_snake(code_), check_list=check_list))
    # 遍历当前字段下规则
    for check in field.xpath('./check'):
        desc_ = check.get('desc')
        type_ = check.get('type')
        # 让没有取到的条件不要为None
        con1_: str = check.get('c1')
        if con1_ is None:
            con1_ = ""
        con2_: str = check.get('c2')
        if con2_ is None:
            con2_ = ""
        con3_: str = check.get('c3')
        if con3_ is None:
            con3_ = ""
        # 检测规则设置的是否正确
        if (("1" in type_) and (con1_ == "")) or (("2" in type_) and (con2_ == "")) or (
                ("3" in type_) and (con3_ == "")):
            # 不正确就阻断执行
            raise SystemExit(f"规则【{field.get('desc')} {desc_}】不正确：type未与条件对应")
        # 存入各个规则
        value_ = check.get('value')
        check_list.append(CheckDo(type_, desc_, con1_, con2_, con3_, value_))

out_spilt_line("插入赋值表SQL")
check_id = 0  # SQL的开始主键
for field in field_list:
    for check in field.check_list:
        check_id += 1
        # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
        print(f"""-- {field.desc} {check.desc}
INSERT INTO DEF_SUBMIT_PARAM(PARAM_ID, RULE_TYPE, COLOR, HEAD_TYPE, LEVEL, PARAM_NAME, PARAM_COMMENT, PARAM_VALUE)
VALUES ('{check_id}', '{check.type}', '{check.con_1}', '{check.con_2}', '{check.con_3}', '{field.java_name}', '{field.desc}', '{check.value}');""")

out_spilt_line("Java的set方法调用")
for field in field_list:
    java_name = field.java_name
    method_name = java_name[0].upper() + java_name[1:]
    # 注解1：这里的submitMap是从数据库查询：key为字段名，value为具体数值
    # 注解2：submitMap的查询是通过条件类型+具体条件，比如传参 color=orange ,headType=圆头,level=lv1 ，
    #       然后按照ruleType=0、1、2、1+2这样挨个查一遍，每查一遍都设一下map，让同名字段的新数值覆盖旧的
    print(f'haJiMi.set{method_name}(submitMap.get("{java_name}")); // {field.desc}')

out_spilt_line("Update方法的SET参数")
for field in field_list:
    print(f'<isNotEmpty property="{field.java_name}" prepend=",">{field.sql_field}=#{field.java_name}#</isNotEmpty>')
