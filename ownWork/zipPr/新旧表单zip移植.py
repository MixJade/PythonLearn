# coding=utf-8
# @Time    : 2026/05/13
# @Software: PyCharm
"""
① 输入老zip路径 → 输入新zip路径
② 解压老zip、新zip 各到同名文件夹
③ 分别读取两个目录下的 desForm.json
   - 校验各自只含 1 个元素
   - 提取 老formId、新formId
④ 初始替换规则：老formId → 新formId
   再扫描老zip目录中的 desFormLayout.json、desFormControl.json
   提取所有 layoutId / formFieldId，生成新的替换ID（用 get_time_id 生成）
⑤ 在老zip解压目录执行全文本替换（所有文件）
⑥ 将改动后的 desFormLayout.json、desFormControl.json
   覆盖到新zip解压目录（不存在则直接复制进去）
⑦ 将新zip解压目录重新打包 → 输出为 原新zip文件名_merged.zip
⑧ 删除两个临时解压目录
"""

import os
import json
import shutil
import zipfile
from datetime import datetime


def get_time_id(i: int) -> str:
    """用当前时间生成时间戳ID，格式如 2024030717275001"""
    now_time: str = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{now_time}0{i}"


# ===================== 解压 =====================

def unzip_file(zip_path: str) -> str:
    """解压 zip 到同名文件夹，返回解压目录路径"""
    if not zip_path.endswith(".zip"):
        raise ValueError(f"不是有效的 zip 文件：{zip_path}")
    extract_path = zip_path[:-4]
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_path)
    print(f"解压完成：{zip_path}  →  {extract_path}")
    return extract_path


# ===================== 提取 formId =====================

def extract_form_id(extract_dir: str) -> str:
    """
    从解压目录中读取 desForm.json，校验只有一个元素，返回 formId
    """
    form_json_path = os.path.join(extract_dir, "desForm.json")
    if not os.path.exists(form_json_path):
        raise FileNotFoundError(f"未找到 desForm.json：{form_json_path}")

    with open(form_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("desForm.json 顶层结构应为 JSON 列表")
    if len(data) != 1:
        raise ValueError(f"desForm.json 应只有 1 个元素，实际有 {len(data)} 个")

    item = data[0]
    if 'formId' not in item:
        raise KeyError("desForm.json 中的元素缺少 'formId' 字段")

    form_id = item['formId']
    print(f"提取到 formId：{form_id}")
    return form_id


# ===================== 替换布局ID（来自脚本2）=====================

def modify_form_id_in_json(
    root_folder: str,
    replace_map: dict,
    filename_list: list
) -> dict:
    """
    读取指定 JSON 文件中的 layoutId / formFieldId，生成新的替换规则
    """
    i = 0
    for read_filename in filename_list:
        file_path = os.path.join(root_folder, read_filename)
        if not os.path.exists(file_path):
            print(f"[警告] 文件不存在，跳过：{file_path}")
            continue
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    if 'layoutId' in item and item['layoutId'] not in replace_map:
                        i += 1
                        replace_map[item['layoutId']] = "123" + get_time_id(i)
                    if 'formFieldId' in item:
                        i += 1
                        replace_map[item['formFieldId']] = "123" + get_time_id(i)
        return replace_map
    return replace_map


def batch_replace_file_content(root_folder: str, replace_map: dict) -> None:
    """
    批量替换文件夹下所有文件的内容
    """
    for root, dirs, files in os.walk(root_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception as e:
                print(f"[警告] 读取文件失败，跳过：{file_path}  ({e})")
                continue

            replaced = False
            operator_map = {}
            for old_str, new_str in replace_map.items():
                if old_str in content:
                    content = content.replace(old_str, new_str)
                    replaced = True
                    operator_map[old_str] = new_str

            if replaced:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"已替换：{file_path}")
                for old_str, new_str in operator_map.items():
                    print(f"\t{old_str}  -->  {new_str}")
            else:
                print(f"无匹配内容：{file_path}")


# ===================== 覆盖文件到新zip解压目录 =====================

def copy_files_to_new_dir(
    src_dir: str,
    dst_dir: str,
    filename_list: list
) -> None:
    """
    将 src_dir 下的指定文件覆盖到 dst_dir（dst_dir 中可以没有这些文件）
    """
    for filename in filename_list:
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename)
        if not os.path.exists(src_path):
            print(f"[警告] 源文件不存在，跳过覆盖：{src_path}")
            continue
        shutil.copy2(src_path, dst_path)
        print(f"已覆盖到新zip目录：{dst_path}")


# ===================== 压缩文件夹 =====================

def zip_folder(source_folder: str, output_zip_path: str) -> None:
    """
    将 source_folder 的内容压缩为 output_zip_path（不含顶层文件夹名）
    """
    # shutil.make_archive 的 root_dir 参数控制压缩内容的根路径
    base_name = output_zip_path[:-4] if output_zip_path.endswith(".zip") else output_zip_path
    shutil.make_archive(base_name, "zip", root_dir=source_folder)
    print(f"压缩完成：{output_zip_path}")


# ===================== 主流程 =====================

def main():
    print("=" * 50)
    print("  zip 合并工具：老zip布局ID替换 → 更新新zip")
    print("=" * 50)

    # 1. 输入文件路径
    old_zip = input("\n请输入【老zip】文件路径：").strip().strip('"').strip("'")
    new_zip = input("请输入【新zip】文件路径：").strip().strip('"').strip("'")

    for path in [old_zip, new_zip]:
        if not os.path.exists(path):
            print(f"[错误] 文件不存在：{path}")
            return

    # 2. 解压两个zip
    print("\n--- 解压文件 ---")
    old_dir = unzip_file(old_zip)
    new_dir = unzip_file(new_zip)

    try:
        # 3. 从老zip解压目录提取 formId（desForm.json 中唯一元素）
        print("\n--- 提取 formId ---")
        old_form_id = extract_form_id(old_dir)
        new_form_id = extract_form_id(new_dir)

        # 4. 构建初始替换规则：老formId → 新formId
        replace_map = {old_form_id: new_form_id}
        print(f"\n初始替换规则：{old_form_id}  -->  {new_form_id}")

        # 5. 从老zip的 desFormLayout.json / desFormControl.json 中提取布局ID，补充替换规则
        target_files = ["desFormLayout.json", "desFormControl.json"]
        print("\n--- 从老zip提取布局ID替换规则 ---")
        replace_map = modify_form_id_in_json(old_dir, replace_map, target_files)
        print(f"替换规则共 {len(replace_map)} 条")

        # 6. 在老zip解压目录执行批量替换（只改 desFormLayout.json、desFormControl.json）
        print("\n--- 替换老zip中的布局ID ---")
        batch_replace_file_content(root_folder=old_dir, replace_map=replace_map)

        # 7. 将修改后的文件覆盖到新zip解压目录
        print("\n--- 将改动文件覆盖进新zip目录 ---")
        copy_files_to_new_dir(old_dir, new_dir, target_files)

        # 8. 将新zip解压目录重新压缩，输出文件名加 _merged 后缀
        print("\n--- 重新压缩新zip目录 ---")
        new_zip_dir = os.path.dirname(new_zip)
        new_zip_basename = os.path.splitext(os.path.basename(new_zip))[0]
        output_zip = os.path.join(new_zip_dir, new_zip_basename + "_merged.zip")
        zip_folder(new_dir, output_zip)

    finally:
        # 9. 删除临时解压目录
        print("\n--- 清理临时解压目录 ---")
        for tmp_dir in [old_dir, new_dir]:
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
                print(f"已删除：{tmp_dir}")

    print("\n✅ 全部完成！")
    print(f"   输出文件：{output_zip}")


if __name__ == "__main__":
    print(__doc__)
    main()
