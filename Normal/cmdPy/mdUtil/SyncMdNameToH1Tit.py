# coding=utf-8
# @Time    : 2024/2/22 17:45
# @Software: PyCharm
import os


def sync_single_file(file_path: str) -> None:
    """将单个 md 文件的文件名同步为 H1 标题

    :param file_path: md 文件的完整路径
    """
    filename = os.path.basename(file_path)
    if not filename.endswith(".md"):
        print(f"[跳过] 不是 md 文件：{file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        lines: list[str] = f.readlines()

    # 删除已有的 H1 标题行
    if lines and lines[0].startswith("# "):
        lines.pop(0)
    # 删除文件开头的空行
    end: int = next((i for i, x in enumerate(lines) if x != '\n'), None)
    if end:
        del lines[0:end]
    # 插入新标题
    lines.insert(0, f"# {filename.replace('.md', '')}\n\n")

    with open(file_path, 'w', encoding='utf-8') as f:
        print(f"--> {filename}")
        f.writelines(lines)


def up_md_title(directory: str) -> None:
    """遍历文件夹下（不含子文件夹）的 md 文件，将文件名同步为 H1 标题

    :param directory: 存有 md 的文件夹路径
    """
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            sync_single_file(os.path.join(directory, filename))


def walk_dir(dir_path: str) -> None:
    """递归遍历文件夹及所有子文件夹，处理每层的 md 文件

    :param dir_path: 根文件夹路径
    """
    print(dir_path)
    up_md_title(dir_path)
    for root, dirs, files in os.walk(dir_path):
        for son_dir in dirs:
            walk_dir(os.path.join(root, son_dir))


def main() -> None:
    print("用法：输入文件路径或文件夹路径")
    print("  输入文件路径  → 只处理该文件（单文件模式，程序会提前说明）")
    print("  输入文件夹路径 → 递归处理该文件夹下所有 md 文件")
    target = input("请输入文件或文件夹路径：").strip()

    if os.path.isfile(target):
        # ---- 单文件模式 ----
        print(f"[单文件模式] 仅处理：{target}")
        sync_single_file(target)
    elif os.path.isdir(target):
        # ---- 文件夹模式（递归）----
        walk_dir(target)
    else:
        print(f"[错误] 路径不存在：{target}")


if __name__ == "__main__":
    main()
