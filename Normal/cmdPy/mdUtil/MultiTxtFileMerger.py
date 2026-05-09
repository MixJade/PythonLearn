# coding=utf-8
# @Time    : 2026-05-09 10:08:51
# @Software: PyCharm
import os
import re

"""多文件合并
1. 检测文件夹下所有文件的后缀名，如果后缀名称不一致则终止合并并提示 
2. 合并txt时加入选项：将文件名作为章节标题
3. 合并md加入选项：降级原标题级别
"""


def _resolve_dir(path: str) -> str:
    """将「文件夹路径」或「文件夹内某文件路径」统一解析为文件夹路径。"""
    path = path.strip().strip('"').strip("'")
    if os.path.isdir(path):
        return path
    parent = os.path.dirname(path)
    if os.path.isdir(parent):
        return parent
    raise ValueError(f"无法解析为有效文件夹路径：{path}")


def _collect_files(dir_path: str) -> list[str]:
    """返回文件夹下所有文件名（非递归，已排序）。"""
    return sorted(
        f for f in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, f))
    )


def _check_extensions(files: list[str]) -> str:
    """
    检测文件后缀一致性。
    返回统一的后缀（小写，含点，如 '.sql'）；不一致则抛出异常。
    """
    exts = {os.path.splitext(f)[1].lower() for f in files}
    exts.discard('')  # 忽略无后缀文件
    if len(exts) > 1:
        raise ValueError(
            f"文件夹中存在多种后缀，无法合并：{', '.join(sorted(exts))}\n"
            "请确保文件夹内所有文件后缀一致。"
        )
    if not exts:
        raise ValueError("文件夹中没有可识别后缀的文件。")
    return exts.pop()


def _ask(prompt: str) -> bool:
    """向用户提问是/否，输入 1 返回 True，其他返回 False。"""
    ans = input(prompt + " [1是/0否]: ").strip()
    return ans == '1'


# ──────────────────────────────────────────────
#  标题降级（md 专用）
# ──────────────────────────────────────────────

def _downgrade_headings(line: str) -> str:
    """将 md 标题降一级（# → ##），最深只处理到五级（六级已是最低不降）。"""
    stripped = line.rstrip('\n')
    match = re.match(r'^(#{1,5})( .+)', stripped)
    if match:
        hashes, rest = match.groups()
        return '#' + hashes + rest + '\n'
    return line


# ──────────────────────────────────────────────
#  各格式合并逻辑
# ──────────────────────────────────────────────

def _merge_txt(dir_path: str, files: list[str], output_path: str, use_filename_as_title: bool) -> int:
    """合并 TXT 文件，可选将文件名作为章节标题。"""
    count = 0
    with open(output_path, 'w', encoding='utf-8') as out:
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            count += 1
            if use_filename_as_title:
                title = os.path.splitext(file_name)[0]
                out.write(f"# {title}\n\n")
            with open(file_path, 'r', encoding='utf-8') as inp:
                out.write(inp.read())
            out.write('\n')
    return count


def _merge_md(dir_path: str, files: list[str], output_path: str, downgrade_headings: bool) -> int:
    """合并 MD 文件，可选原标题降级。"""
    output_name = os.path.basename(output_path)
    count = 0
    with open(output_path, 'w', encoding='utf-8') as out:
        if downgrade_headings:
            title = os.path.splitext(output_name)[0]
            out.write(f"# {title}\n")  # 原标题降级则以文件名作为大标题
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            count += 1
            # 文件间插入空行（首个文件除外）
            if count > 1:
                out.write('\n')
            with open(file_path, 'r', encoding='utf-8') as inp:
                for line in inp:
                    if downgrade_headings:
                        line = _downgrade_headings(line)
                    out.write(line)
    return count


def _merge_generic(dir_path: str, files: list[str], output_path: str) -> int:
    """通用合并：直接拼接，文件间加空行。"""
    count = 0
    with open(output_path, 'w', encoding='utf-8') as out:
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            count += 1
            if count > 1:
                out.write('\n')
            with open(file_path, 'r', encoding='utf-8') as inp:
                content = inp.read()
                out.write(content)
                if content and not content.endswith('\n'):
                    out.write('\n')
    return count


# ──────────────────────────────────────────────
#  主入口
# ──────────────────────────────────────────────

def main() -> None:
    print("=" * 50)
    print("  多文件合并工具")
    print("=" * 50)

    # 1. 输入路径
    raw_path = input("请输入待合并的文件夹路径（或文件夹内某个文件路径）：").strip()
    try:
        dir_path = _resolve_dir(raw_path)
    except ValueError as e:
        print(f"[错误] {e}")
        return

    print(f"文件夹路径：{dir_path}")

    # 2. 收集文件 & 后缀检测
    files = _collect_files(dir_path)
    if not files:
        print("[错误] 文件夹内没有文件。")
        return

    try:
        ext = _check_extensions(files)
    except ValueError as e:
        print(f"[终止] {e}")
        return

    print(f"检测到文件后缀：{ext}，共 {len(files)} 个文件")

    # 3. 输入文件名并拼接输出路径
    default_name = f"多文件合并_结果{ext}"
    output_name = input(f"请输入生成的文件名称（直接回车使用默认：{default_name}）：").strip()
    if not output_name:
        output_name = default_name
    # 确保后缀与源文件一致
    if not output_name.lower().endswith(ext):
        output_name = output_name + ext
    parent_dir = os.path.dirname(dir_path)  # 输出文件保存在文件夹的同级目录
    output_path = os.path.join(parent_dir, output_name)

    # 4. 根据后缀走不同逻辑
    ext_lower = ext.lower()

    use_filename_as_title = False
    downgrade_headings = False

    if ext_lower == '.txt':
        use_filename_as_title = _ask("是否将文件名作为章节标题")
    if ext_lower == '.md':
        downgrade_headings = _ask("是否将原文件中的标题降级（# → ##）")

    # 5. 执行合并
    try:
        if ext_lower == '.txt':
            count = _merge_txt(dir_path, files, output_path, use_filename_as_title)
        elif ext_lower == '.md':
            count = _merge_md(dir_path, files, output_path, downgrade_headings)
        else:
            count = _merge_generic(dir_path, files, output_path)
    except Exception as e:
        print(f"[错误] 合并过程中出现异常：{e}")
        return

    print(f"\n✅ 合并完成！共合并 {count} 个文件，已输出至上一级目录：\n   {output_path}")


if __name__ == '__main__':
    main()
