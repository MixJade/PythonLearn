# coding=utf-8
# @Time    : 2025/11/25 14:54
# @Software: PyCharm
import os


def batch_replace_file_content(
        root_folder,
        replace_map,
        encoding="utf-8",
        exclude_extensions=None,
        exclude_files=None,
):
    """
    批量替换文件夹下所有文件的内容
    :param root_folder: 目标文件夹路径（绝对/相对路径均可）
    :param replace_map: 替换规则字典，格式：{待替换字符串: 目标字符串}
    :param encoding: 文件编码（默认 utf-8，需根据实际文件调整，如 gbk）
    :param exclude_extensions: 跳过的文件后缀列表（如 [".zip", ".exe"]）
    :param exclude_files: 跳过的文件名列表（如 ["config.json", "README.md"]）
    """
    # 初始化默认排除列表
    if exclude_extensions is None:
        exclude_extensions = []
    if exclude_files is None:
        exclude_files = []

    # 遍历文件夹
    for root, dirs, files in os.walk(root_folder):
        for filename in files:
            # 跳过指定文件
            if filename in exclude_files:
                print(f"跳过文件：{os.path.join(root, filename)}")
                continue

            # 跳过指定后缀的文件（避免修改二进制文件如图片、压缩包）
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext in exclude_extensions:
                print(f"跳过后缀：{os.path.join(root, filename)}")
                continue

            # 拼接文件完整路径
            file_path = os.path.join(root, filename)

            try:
                # 读取文件内容
                with open(file_path, "r", encoding=encoding, errors="ignore") as f:
                    content = f.read()

                # 标记是否有替换操作
                replaced = False
                # 执行批量替换（按 replace_map 中的规则）
                for old_str, new_str in replace_map.items():
                    if old_str in content:
                        content = content.replace(old_str, new_str)
                        replaced = True

                # 若有替换，写入新内容（覆盖原文件）
                if replaced:
                    with open(file_path, "w", encoding=encoding) as f:
                        f.write(content)
                    print(f"已替换：{file_path}")
                else:
                    print(f"无匹配内容：{file_path}")

            except Exception as e:
                # 捕获异常（如权限不足、文件被占用等）
                print(f"处理失败：{file_path} -> 错误：{str(e)}")


# ------------------- 示例调用 -------------------
if __name__ == "__main__":
    # 1. 配置参数
    TARGET_FOLDER = "测试解压"  # 待处理的文件夹路径
    REPLACE_RULES = {
        "old文本": "new文本",
    }
    # 跳过的文件后缀（避免修改二进制文件）
    EXCLUDE_EXT = [".zip", ".rar", ".exe", ".png", ".jpg", ".jpeg", ".gif", ".bin"]
    # 跳过的特定文件
    EXCLUDE_FILES = ["backup.txt", "log.log"]

    # 2. 执行批量替换
    batch_replace_file_content(
        root_folder=TARGET_FOLDER,
        replace_map=REPLACE_RULES,
        encoding="utf-8",  # 若文件是 gbk 编码，改为 encoding="gbk"
        exclude_extensions=EXCLUDE_EXT,
        exclude_files=EXCLUDE_FILES
    )

    print("\n批量替换完成！")
