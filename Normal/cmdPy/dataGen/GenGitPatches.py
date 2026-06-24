# coding=utf-8
# @Time    : 2026/6/24 16:24
# @Software: PyCharm
"""
从指定Git仓库提取某个提交及其之后所有提交的patch文件，保存到桌面。
文件名使用提交的中文标题，不出现乱码。
"""
import os
import re
import subprocess
import datetime


def is_valid_git_repo(path: str) -> bool:
    """校验路径是否为有效的Git仓库"""
    if not os.path.exists(path):
        return False
    git_dir = os.path.join(os.path.abspath(path), ".git")
    return os.path.isdir(git_dir)


def get_desktop_path() -> str:
    """获取桌面路径（兼容中文/英文系统）"""
    home = os.path.expanduser("~")
    for name in ("Desktop", "桌面"):
        path = os.path.join(home, name)
        if os.path.isdir(path):
            return path


def sanitize_filename(name: str) -> str:
    """将提交信息转为合法的文件名，去除特殊字符"""
    # 替换Windows不允许的字符
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
    name = re.sub(invalid_chars, '_', name)
    # 去除首尾空格和点号（Windows不允许文件名末尾是点或空格）
    name = name.strip().rstrip('.')
    # 截断过长文件名（留空间给序号和hash前缀）
    if len(name) > 150:
        name = name[:150]
    return name


def git_run(repo_path: str, args: list[str], encoding: str = "utf-8") -> subprocess.CompletedProcess:
    """在指定仓库路径下执行git命令"""
    return subprocess.run(
        ["git", "-C", repo_path] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding=encoding,
    )


def get_commit_list(repo_path: str, start_hash: str) -> list[str]:
    """
    获取从start_hash到HEAD的所有提交hash（含start_hash本身），按时间正序排列。
    """
    # 先尝试 start_hash^..HEAD（包含start_hash及其之后的提交）
    result = git_run(repo_path, ["rev-list", "--reverse", f"{start_hash}^..HEAD"])
    if result.returncode == 0 and result.stdout.strip():
        commits = [h.strip() for h in result.stdout.strip().split("\n") if h.strip()]
        return commits

    # 如果start_hash是根提交（没有父提交），^..HEAD会失败
    # 改用 start_hash..HEAD 获取之后的提交，再手动加上 start_hash
    result = git_run(repo_path, ["rev-list", "--reverse", f"{start_hash}..HEAD"])
    after_commits = [h.strip() for h in result.stdout.strip().split("\n") if
                     h.strip()] if result.returncode == 0 else []
    return [start_hash] + after_commits


def generate_patches(repo_path: str, start_hash: str, output_dir: str) -> None:
    """为每个提交生成patch文件，文件名使用提交中文标题"""
    commits = get_commit_list(repo_path, start_hash)
    if not commits:
        print("未找到提交记录。")
        return

    print(f"共找到 {len(commits)} 个提交，开始生成patch...")

    success_count = 0
    for idx, hash_val in enumerate(commits, 1):
        # 获取提交的短hash
        short_result = git_run(repo_path, ["rev-parse", "--short", hash_val])
        if short_result.returncode != 0:
            print(f"  [{idx}] 获取短hash失败：{hash_val}")
            continue
        short_hash = short_result.stdout.strip()

        # 获取提交标题（subject）
        subject_result = git_run(repo_path, ["log", "-1", "--format=%s", hash_val])
        if subject_result.returncode != 0:
            print(f"  [{idx}] 获取提交标题失败：{hash_val}")
            continue
        subject = subject_result.stdout.strip()

        # 构建文件名：序号 + 短hash + 提交标题
        safe_subject = sanitize_filename(subject)
        filename = f"{idx:03d}-{short_hash}-{safe_subject}.patch"
        filepath = os.path.join(output_dir, filename)

        # 生成patch内容
        patch_result = git_run(repo_path, ["format-patch", "-1", "--stdout", hash_val])
        if patch_result.returncode != 0:
            print(f"  [{idx}] 生成patch失败：{short_hash} {subject}")
            print(f"       错误：{patch_result.stderr.strip()}")
            continue

        # 写入文件（使用utf-8编码确保中文不乱码）
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(patch_result.stdout)

        success_count += 1
        print(f"  [{idx}] ✅ {filename}")

    print(f"\n完成！成功生成 {success_count}/{len(commits)} 个patch文件。")


def main():
    # ========== 1. 输入项目路径 ==========
    project_path = input("请输入项目路径：").strip()
    if not project_path:
        print("未输入路径，程序结束。")
        return

    abs_path = os.path.abspath(project_path)
    if not is_valid_git_repo(abs_path):
        print(f"❌ {abs_path} 不是有效的Git仓库，请检查路径。")
        return

    # ========== 2. 输入提交hash ==========
    commit_hash = input("请输入提交hash值（不输入则使用最新提交）：").strip()

    if not commit_hash:
        # 获取HEAD最新提交的hash
        result = git_run(abs_path, ["rev-parse", "HEAD"])
        if result.returncode != 0:
            print("❌ 获取最新提交hash失败。")
            return
        commit_hash = result.stdout.strip()
        # 同时获取短hash方便显示
        short_result = git_run(abs_path, ["rev-parse", "--short", commit_hash])
        short_hash_display = short_result.stdout.strip() if short_result.returncode == 0 else commit_hash[:7]
        print(f"使用最新提交：{short_hash_display}")
    else:
        # 验证hash是否有效，并转为完整hash
        verify_result = git_run(abs_path, ["rev-parse", "--verify", commit_hash])
        if verify_result.returncode != 0:
            print(f"❌ 提交hash '{commit_hash}' 不存在或无效。")
            return
        commit_hash = verify_result.stdout.strip()

    # ========== 3. 创建输出目录 ==========
    project_name = os.path.basename(os.path.normpath(abs_path))
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    desktop_path = get_desktop_path()
    output_folder = os.path.join(desktop_path, f"{project_name}{current_date}")

    os.makedirs(output_folder, exist_ok=True)
    print(f"\n输出目录：{output_folder}")

    # ========== 4. 生成patch ==========
    generate_patches(abs_path, commit_hash, output_folder)

    print(f"patch文件保存在：{output_folder}")


if __name__ == "__main__":
    main()
