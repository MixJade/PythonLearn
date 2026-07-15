# coding=utf-8
# @Time    : 2026/07/15
# @Software: PyCharm
"""
dy-form-util 入口脚本

功能菜单：
  1. 表单数据移植（老zip布局ID替换 -> 更新新zip）
  2. 探查 desFormControl.json -> Markdown 表格
  3. zip 解压 / 压缩
"""

import form_migrate
import form_inspect


def show_menu():
    print()
    print("=" * 50)
    print("  dy-form-util 工具集")
    print("=" * 50)
    print("  1. 探查表单zip字段 (输出md表格)")
    print("  2. 表单zip布局样式移植")
    print("  0. 退出")
    print()


def main():
    show_menu()
    choice = input("请选择功能: ").strip()

    if choice == "1":
        form_inspect.run()
    elif choice == "2":
        form_migrate.run()
    else:
        print("再见！")


if __name__ == "__main__":
    main()
