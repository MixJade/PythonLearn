# coding=utf-8
# @Time    : 2025/9/12 16:26
# @Software: PyCharm
from collections import defaultdict
from typing import NamedTuple


class Role(NamedTuple):
    """按钮的角色
    """
    roleNo: str
    roleName: str


class Btn(NamedTuple):
    """按钮
    """
    btnName: str
    roleList: list[Role]


class Menu(NamedTuple):
    """按钮所属菜单
    """
    menuNo: str
    desc: str
    btnList: list[Btn]


def out_hy_menu_btn_sql(menu: Menu, is_hy=True):
    """输出菜单下按钮的核对、检查sql
    """
    hy_txt, menu_check_num = '检查', 0
    if is_hy:
        hy_txt, menu_check_num = '核对', len(menu.btnList)
    menu_btn_res = ", ".join(f"'{btn.btnName}'" for btn in menu.btnList)
    # 开始输出菜单按钮检查
    print(f"\n-- {hy_txt} {menu.desc}菜单按钮 预计{menu_check_num}条")
    # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
    print(f"""SELECT *
FROM SYS_BUTTON
WHERE MENU_NO = '{menu.menuNo}'
  AND BUTTON_NO IN ({menu_btn_res});""")

    # 统计角色与按钮的关系
    role_btn_map = defaultdict(list[Btn])
    role_name_map = {}
    for btn in menu.btnList:
        for role in btn.roleList:
            role_btn_map[role.roleNo].append(btn)
            role_name_map[role.roleNo] = role.roleName

    for role_no, role_btn_list in role_btn_map.items():
        role_check_num = len(role_btn_list) if is_hy else 0
        role_btn_res = ", ".join(f"'{btn.btnName}'" for btn in role_btn_list)
        # 按钮下角色的核对、检查sql
        print(f"\n-- {hy_txt} {menu.desc}的{role_name_map.get(role_no)}权限 预计{role_check_num}条")
        # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
        print(f"""SELECT *
FROM SYS_ROLE_BUTTON
WHERE MENU_NO = '{menu.menuNo}'
  AND ROLE_NO = '{role_no}'
  AND BUTTON_NO IN ({role_btn_res});""")


def out_insert_menu_btn_sql(menu: Menu):
    """输出菜单下按钮的按钮的sql
    """
    print(f"\n-- {menu.desc}菜单新增按钮")
    for btn in menu.btnList:
        print("-- 预计1条")
        # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
        print("INSERT INTO SYS_BUTTON (MENU_NO, BUTTON_NO, BUTTON_DESC)")
        print(f"VALUES ('{menu.menuNo}', '{btn.btnName}', '{menu.desc}——>{btn.btnName}');")

    # 统计角色与按钮的关系
    role_btn_map = defaultdict(list[Btn])
    role_name_map = {}
    for btn in menu.btnList:
        for role in btn.roleList:
            role_btn_map[role.roleNo].append(btn)
            role_name_map[role.roleNo] = role.roleName

    for role_no, role_btn_list in role_btn_map.items():
        # 按钮下角色的核对、检查sql
        print(f"\n-- ({menu.desc})为{role_no}{role_name_map.get(role_no)}插入权限")
        for role_btn in role_btn_list:
            print("-- 预计1条")
            # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
            print("INSERT INTO SYS_ROLE_BUTTON (ID, ROLE_NO, MENU_NO, BUTTON_NO)")
            print(f"VALUES (sys_role_button_seq.nextval, '{role_no}', '{menu.menuNo}', '{role_btn.btnName}');")
