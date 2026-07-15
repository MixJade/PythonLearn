# coding=utf-8
# @Time    : 2026/07/15
# @Software: PyCharm
"""
zip 工具模块 —— 解压 / 压缩

可被其他脚本 import 使用，也可通过命令行单独调用：

  解压:  python zip_util.py unzip <zip文件路径> [-d 目标目录]
  压缩:  python zip_util.py zip <文件夹路径> [-o 输出zip路径]
"""

import os
import shutil
import zipfile


# ===================== 解压 =====================

def unzip_file(zip_path: str, extract_dir: str = None) -> str:
    """
    解压 zip 到同名文件夹（或指定目录），返回解压目录路径。

    :param zip_path:   zip 文件路径
    :param extract_dir: 解压目标目录，为 None 时自动取 zip 同名文件夹
    :return: 解压后的目录路径
    """
    if not zip_path.endswith(".zip"):
        raise ValueError(f"不是有效的 zip 文件：{zip_path}")
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"文件不存在：{zip_path}")

    if extract_dir is None:
        extract_dir = zip_path[:-4]  # 去掉 .zip 后缀

    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_dir)
    print(f"解压完成：{zip_path}  ->  {extract_dir}")
    return extract_dir


# ===================== 压缩 =====================

def zip_folder(source_folder: str, output_zip_path: str) -> None:
    """
    将 source_folder 的内容压缩为 output_zip_path（不含顶层文件夹名）。

    :param source_folder:   要压缩的文件夹
    :param output_zip_path: 输出 zip 文件路径
    """
    base_name = output_zip_path[:-4] if output_zip_path.endswith(".zip") else output_zip_path
    shutil.make_archive(base_name, "zip", root_dir=source_folder)
    print(f"压缩完成：{output_zip_path}")


# ===================== 校验单表单 zip =====================

def validate_single_form_zip(zip_path: str) -> None:
    """
    校验 zip 中的 desForm.json 只有 1 个元素（即只包含单个表单）。
    不通过则直接抛出 ValueError。

    :param zip_path: zip 文件路径
    """
    import json

    if not zip_path.lower().endswith(".zip"):
        return  # 非 zip 不校验，由调用方自行处理

    try:
        raw = read_file_from_zip(zip_path, "desForm.json")
        data = json.loads(raw)
    except KeyError:
        raise FileNotFoundError(f"zip 中未找到 desForm.json：{zip_path}")
    except Exception as e:
        raise ValueError(f"读取 desForm.json 失败：{e}")

    if not isinstance(data, list) or len(data) != 1:
        raise ValueError(
            f"zip 中 desForm.json 包含 {len(data) if isinstance(data, list) else '?'} 个表单，"
            f"仅支持单个表单的 zip！请确认输入的 zip 为单个表单。"
        )


# ===================== 从 zip 中读取单个文件内容 =====================

def read_file_from_zip(zip_path: str, inner_filename: str) -> str:
    """
    直接从 zip 中读取指定文件的文本内容（不解压到磁盘）。

    :param zip_path:       zip 文件路径
    :param inner_filename: zip 内的文件名
    :return: 文件文本内容
    """
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        return zipf.read(inner_filename).decode('utf-8')


# ===================== 命令行入口 =====================

def _cmd_unzip(args):
    zip_path = args.zip_path
    if not os.path.exists(zip_path):
        print(f"[错误] 文件不存在：{zip_path}")
        return
    try:
        unzip_file(zip_path, args.dir)
    except Exception as e:
        print(f"[错误] {e}")


def _cmd_zip(args):
    folder = args.folder
    if not os.path.exists(folder):
        print(f"[错误] 文件夹不存在：{folder}")
        return
    output = args.output or (folder.rstrip('/\\') + ".zip")
    try:
        zip_folder(folder, output)
    except Exception as e:
        print(f"[错误] {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="zip 解压 / 压缩工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # 解压: python zip_util.py unzip <zip> [-d dir]
    p_unzip = subparsers.add_parser("unzip", help="解压 zip 文件")
    p_unzip.add_argument("zip_path", help="zip 文件路径")
    p_unzip.add_argument("-d", "--dir", dest="dir", default=None, help="解压目标目录（默认取 zip 同名文件夹）")
    p_unzip.set_defaults(func=_cmd_unzip)

    # 压缩: python zip_util.py zip <folder> [-o output]
    p_zip = subparsers.add_parser("zip", help="压缩文件夹为 zip")
    p_zip.add_argument("folder", help="要压缩的文件夹路径")
    p_zip.add_argument("-o", "--output", dest="output", default=None, help="输出 zip 文件路径（默认 folder.zip）")
    p_zip.set_defaults(func=_cmd_zip)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
    else:
        args.func(args)
