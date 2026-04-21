# coding=utf-8
# @Time    : 2026/4/21 10:19
# @Software: PyCharm
import json
import os
import shutil
import sys
import zipfile

# 获取当前 b.py 所在的文件夹路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# 把这个路径加入系统搜索路径，解决绝对路径运行找不到 a 的问题
sys.path.insert(0, script_dir)
_local_zip_path: str = ""   # 最终确认的 zip 路径


def _load_zip_path_from_config() -> str:
    """从命令行传入的 JSON 配置文件中读取 local_jar_path（必须是 .zip 路径）"""
    if len(sys.argv) < 2:
        print("⚠️  未传入配置文件路径，before_run 将跳过 zip 检测")
        return ""
    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"❌ 配置文件不存在: {json_path}")
        sys.exit(1)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {e}")
        sys.exit(1)
    zip_path = cfg.get("local_jar_path", "")
    if not zip_path:
        print("❌ 配置文件缺少 'local_jar_path' 字段")
        sys.exit(1)
    if not zip_path.lower().endswith(".zip"):
        print(f"❌ local_jar_path 必须是 .zip 文件路径，当前值: {zip_path}")
        sys.exit(1)
    return zip_path


def before_run():
    """执行前运行的逻辑：
    1. 若 zip 已存在 → 直接放行
    2. 若 zip 不存在 → 查找同名文件夹 → 压缩为 zip
    """
    global _local_zip_path
    print("\n【UI部署脚本 - 前置逻辑】开始执行")
    _local_zip_path = _load_zip_path_from_config()
    if not _local_zip_path:
        print("⚠️  未获取到 zip 路径，跳过前置检测，直接放行")
        return
    zip_dir = os.path.dirname(_local_zip_path)          # 如：D:\proj\frontend\xxx-ui
    zip_filename = os.path.basename(_local_zip_path)     # 如：xxx-ui.zip
    zip_stem = os.path.splitext(zip_filename)[0]         # 如：xxx-ui
    folder_path = os.path.join(zip_dir, zip_stem)        # 如：D:\proj\frontend\xxx-ui\xxx-ui
    print(f"\n=== 检查本地 zip 文件 ===")
    print(f"目标 zip 路径：{_local_zip_path}")
    # ---- 情况1：zip 已存在，直接放行 ----
    if os.path.isfile(_local_zip_path):
        print(f"✅ zip 文件已存在，直接放行：{_local_zip_path}")
        return
    # ---- 情况2：zip 不存在，查找同名文件夹并压缩 ----
    print(f"⚠️  zip 文件不存在，查找同名文件夹：{folder_path}")
    if not os.path.isdir(folder_path):
        print(f"❌ 同名文件夹也不存在：{folder_path}")
        print("    请确认 zip 文件或对应文件夹已就绪后重试。")
        sys.exit(1)
    print(f"📦 发现文件夹，开始压缩 → {_local_zip_path}")
    _compress_folder_to_zip(folder_path, _local_zip_path)
    print(f"✅ 压缩完成：{_local_zip_path}")
    print("【UI部署脚本 - 前置逻辑】执行完毕\n")


def _compress_folder_to_zip(folder_path: str, zip_path: str):
    """将 folder_path 文件夹压缩为 zip_path（zip 根目录为文件夹本身）"""
    parent_dir = os.path.dirname(folder_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                abs_file = os.path.join(root, file)
                # arcname 保留文件夹名作为 zip 内部根目录
                rel_path = os.path.relpath(abs_file, parent_dir)
                zf.write(abs_file, arcname=rel_path)


def after_run():
    """执行后运行的逻辑：
    - 删除同名文件夹
    - 删除生成的 zip 文件
    """
    global _local_zip_path

    print("【UI部署脚本 - 后置逻辑】开始执行")
    zip_dir = os.path.dirname(_local_zip_path)
    zip_stem = os.path.splitext(os.path.basename(_local_zip_path))[0]
    folder_path = os.path.join(zip_dir, zip_stem)
    print(f"\n=== 清理临时文件 ===")
    # 删除同名文件夹
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        print(f"✅ 已删除文件夹：{folder_path}")
    # 删除 zip 文件
    if os.path.isfile(_local_zip_path):
        os.remove(_local_zip_path)
        print(f"✅ 已删除 zip 文件：{_local_zip_path}")
    print("【UI部署脚本 - 后置逻辑】执行完毕\n")


if __name__ == "__main__":
    before_run()
    import auto_deploy_jar
    auto_deploy_jar.main()
    after_run()
