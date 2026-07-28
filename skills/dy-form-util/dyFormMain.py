# coding=utf-8
# @Time    : 2026/07/15
# @Software: PyCharm
"""
dy-form-util 入口脚本

流程：
  1. 探查表单zip字段（输出md表格）
  2. 根据提示选择：0退出 或 2执行表单zip布局样式移植
"""

import os

import form_inspect
import form_migrate


def main():
    # ========== 步骤1: 探查表单zip字段 ==========
    input_path = form_inspect.run()
    if not input_path:
        return

    # ========== 步骤2: 探查完成后，让用户选择 ==========
    print()
    print("=" * 50)
    print("  请选择后续操作：")
    print("  0. 退出")
    print("  2. 表单zip布局样式移植（需追加输入新表单路径）")
    print("=" * 50)

    choice = input("请选择: ").strip()

    if choice == "0":
        print("再见！")
    elif choice == "2":
        # 追加输入新表单路径
        new_zip = input("\n请输入【新zip】文件路径：").strip().strip('"').strip("'")
        if not new_zip:
            print("未输入新表单路径，退出。")
            return
        if not os.path.exists(new_zip):
            print(f"[错误] 文件不存在：{new_zip}")
            return

        # 执行移植，将探查的表单作为老zip，新路径作为新zip
        form_migrate.run_with_paths(old_zip=input_path, new_zip=new_zip)
    else:
        print("无效选择，退出。")


if __name__ == "__main__":
    main()
