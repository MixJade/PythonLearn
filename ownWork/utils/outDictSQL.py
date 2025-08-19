# coding=utf-8
# @Time    : 2025/8/18 10:42
# @Software: PyCharm
from typing import NamedTuple


class DicParam(NamedTuple):
    """单个小参数
    """
    seq: int
    code: str
    name: str


class DicMain(NamedTuple):
    """整个字典
    """
    code: str
    name: str
    is_new: bool
    parm_list: list[DicParam]


def out_hy_dic_sql(dic: DicMain, is_hy=True):
    """输出核对、检查sql
    """
    hy_txt, check_num = '检查', 0
    if is_hy:
        hy_txt, check_num = '核对', len(dic.parm_list)
    end_str = ";"
    if not dic.is_new:
        param_result = ", ".join(f"'{param.code}'" for param in dic.parm_list)
        end_str = f"\n  AND OPT_CODE IN ({param_result});"
    # 开始输出
    print(f"\n-- {hy_txt}字典·{dic.name} 预计{check_num}条")
    # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
    print(f"SELECT *\nFROM PARM_DIC\nWHERE KEY_NAME = '{dic.code}'{end_str}")


def out_insert_dic_sql(dic: DicMain):
    """输出插入字典的sql
    """
    print(f"\n-- 插入字典·{dic.name} 共计{len(dic.parm_list)}条")
    for parm in dic.parm_list:
        # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
        print("INSERT INTO PARM_DIC (KEY_NAME, OPT_CODE, OPT_NAME, SEQN, STS)")
        print(f"VALUES ('{dic.code}', '{parm.code}', '{parm.name}', {parm.seq}, '1');")
