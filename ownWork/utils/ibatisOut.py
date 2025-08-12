# coding=utf-8
# @Time    : 2025/8/12 11:05
# @Software: PyCharm
from typing import NamedTuple


class IBatisParam(NamedTuple):
    sql_column: str  # SQL字段名称,形如:PRJ_NAME
    java_field: str  # 实体类中字段名称,形如:prjName


def out_spilt_line(desc: str):
    """打印分割线"""
    print(f"\n{'=' * 25}【{desc}】{'=' * 25}\n")


def out_update_col(param_list: list[IBatisParam]):
    """输出更新列
    """
    out_spilt_line("更新列")
    for index, param in enumerate(param_list):
        res_str = f'{param.sql_column}=#{param.java_field}#'
        if index != len(param_list) - 1:
            res_str += ","
        print(res_str)


def out_update_cdata_col(param_list: list[IBatisParam]):
    """输出更新列(CDATA格式)
    """
    out_spilt_line("更新列(CDATA格式)")
    print('<dynamic prepend="SET ">')
    for param in param_list:
        print(f'\t<isNotEmpty property="{param.java_field}" prepend=",">'
              f'{param.sql_column}=#{param.java_field}#</isNotEmpty>')
    print('</dynamic>')


def out_insert_col(param_list: list[IBatisParam], out_spilt=False):
    """输出插入列
    """
    if out_spilt:
        out_spilt_line("插入列")
    # noinspection SqlNoDataSourceInspection
    insert_sql = "INSERT INTO XXX("
    # 更新的sql列名
    for idx, val in enumerate(param_list):
        if idx == 0:  # 第一个元素特殊处理
            insert_sql += f"{val.sql_column},\n"
        elif idx == len(param_list) - 1:  # 如果索引等于列表长度减1，说明这是最后一个元素
            insert_sql += f"        {val.sql_column})\nVALUES ("
        else:
            insert_sql += f"        {val.sql_column},\n"
    # 更新的java字段
    for idx, val in enumerate(param_list):
        if idx == 0:  # 第一个元素特殊处理
            insert_sql += f"#{val.java_field}#,\n"
        elif idx == len(param_list) - 1:  # 如果索引等于列表长度减1，说明这是最后一个元素
            insert_sql += f"        #{val.java_field}#)"
        else:
            insert_sql += f"        #{val.java_field}#,\n"
    print(insert_sql)


def out_insert_cdata_col(param_list: list[IBatisParam]):
    """输出插入列(CDATA格式)
    """
    out_spilt_line("插入列(CDATA格式)")
    out_insert_col(param_list, False)


def out_result_map(param_list: list[IBatisParam]):
    """输出结果集
    """
    out_spilt_line("结果集")
    for index, param in enumerate(param_list):
        res_str = f'<result property="{param.java_field}" column="{param.sql_column}"/>'
        print(res_str)


def out_select_col(param_list: list[IBatisParam]):
    """输出查询列
    """
    out_spilt_line("查询列")
    column_list = []
    for param in param_list:
        column_list.append(param.sql_column)
    # 使用 join() 方法将列表元素用逗号连接成字符串
    print(",".join(column_list))
