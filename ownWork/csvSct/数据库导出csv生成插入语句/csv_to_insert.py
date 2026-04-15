# coding=utf-8
# @Time    : 2026/4/14 11:27
# @Software: PyCharm
import os
import re
import csv
import sys

"""
将指定文件夹下所有从数据库导出的 CSV 文件，转换为 INSERT 语句，
并写入脚本同目录下的 "导出的数据_结果.sql"。
"""


# 时间戳格式：YYYY-MM-DD HH:MM:SS[.fff]，末尾可能有空格
_DATETIME_PAT = re.compile(
    r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?\s*$"
)


def escape_sql_value(value: str) -> str:
    """
    将单个字段值转为 SQL 字面量字符串：
    - NULL / 空字符串 → NULL（不加引号）
    - 时间戳格式（TIMESTAMP） → TIMESTAMP '值'（不加单引号）
    - 其他  → 用单引号包裹，内部单引号转义为 ''
    """
    if value is None or value.strip() == "":
        return "NULL"
    if _DATETIME_PAT.match(value):
        # 去除末尾多余空格后再套 TIMESTAMP
        return f"TIMESTAMP '{value.strip()}'"
    # 转义单引号
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def resolve_table_name(filename_no_ext: str) -> str:
    """
    处理表名：若文件名格式为 "表名_纯数字"，则去掉末尾的 "_纯数字" 部分，只保留表名。
    判定条件：以下划线分割后，最后一段全为数字。
    示例：
        user_info_20240101  → user_info
        orders_20231215     → orders
        product             → product（不变）
    """
    parts = filename_no_ext.rsplit("_", 1)
    if len(parts) == 2 and parts[1].isdigit():
        return parts[0]
    return filename_no_ext


def csv_file_to_inserts(csv_path: str) -> list[str]:
    """
    读取一个 CSV 文件，返回对应的 INSERT 语句列表。
    表名取自文件名（不含扩展名），并去除末尾的日期后缀（_纯数字）。
    """
    raw_name = os.path.splitext(os.path.basename(csv_path))[0]
    table_name = resolve_table_name(raw_name)
    statements = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return []
        columns = [col.strip() for col in reader.fieldnames]
        col_list = ", ".join(str(c) for c in columns)
        for row in reader:
            values = [escape_sql_value(row.get(col, "")) for col in columns]
            val_list = ", ".join(values)
            # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
            stmt = f"INSERT INTO {table_name} ({col_list}) VALUES ({val_list});"
            statements.append(stmt)
    return statements


def process_folder(folder_path: str, output_path: str) -> None:
    """
    遍历文件夹中的所有 CSV 文件，生成 INSERT 语句并写入输出文件。
    """
    csv_files = sorted([
        f for f in os.listdir(folder_path)
        if f.lower().endswith(".csv")
    ])
    if not csv_files:
        print("⚠️  该文件夹下未找到任何 CSV 文件，请检查路径。")
        return
    total_rows = 0
    with open(output_path, "w", encoding="utf-8") as out:
        for filename in csv_files:
            csv_path = os.path.join(folder_path, filename)
            print(f"  正在处理：{filename} ...")
            stmts = csv_file_to_inserts(csv_path)
            # 每个文件开始写文件名注释
            out.write(f"-- ============================================================\n")
            out.write(f"-- 文件：{filename}\n")
            out.write(f"-- ============================================================\n")
            if stmts:
                out.write("\n".join(stmts))
                out.write("\n\n")
                total_rows += len(stmts)
                print(f"    → {len(stmts)} 条 INSERT 语句")
            else:
                out.write("-- （该文件无数据行）\n\n")
                print(f"    → 无数据行，跳过")
    print(f"\n✅ 完成！共生成 {total_rows} 条 INSERT 语句。")
    print(f"📄 输出文件：{output_path}")


def main() -> None:
    print("=" * 60)
    print("  CSV → INSERT 语句 转换工具")
    print("=" * 60)
    # 获取输入路径
    folder_path = input("\n请输入包含 CSV 文件的文件夹路径：").strip().strip('"').strip("'")
    # 验证路径
    if not os.path.isdir(folder_path):
        print(f"❌ 路径不存在或不是文件夹：{folder_path}")
        sys.exit(1)
    # 输出文件：脚本同目录下
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "导出的数据_结果.sql")
    print(f"\n源文件夹：{folder_path}")
    print(f"输出文件：{output_path}\n")
    process_folder(folder_path, output_path)


if __name__ == "__main__":
    main()
