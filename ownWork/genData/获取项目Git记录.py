# coding=utf-8
# @Time    : 2026/3/21 21:33
# @Software: PyCharm
import os
import subprocess
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional


def is_valid_git_repo(path: str) -> bool:
    """校验路径是否为有效的Git仓库（存在.git目录）"""
    if not os.path.exists(path):
        return False
    git_dir = os.path.join(os.path.abspath(path), ".git")
    return os.path.isdir(git_dir)


def get_default_date() -> str:
    """获取默认日期：今天的7天前（格式YYYY-MM-DD）"""
    seven_days_ago = datetime.now() - timedelta(days=7)
    return seven_days_ago.strftime("%Y-%m-%d")


def get_commit_branch(repo_path: str, commit_hash: str) -> str:
    """获取单个提交所属的分支（包含本地+远程分支，多个分支用逗号分隔）"""
    result = subprocess.run(
        ["git", "-C", repo_path, "branch", "-a", "--contains", commit_hash],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        check=True
    )
    branches = []
    for line in result.stdout.strip().split("\n"):
        branch_name = line.strip().replace("*", "").strip()
        # 过滤 HEAD 指针行，例如 remotes/origin/HEAD -> origin/master
        if branch_name and "->" not in branch_name and branch_name not in branches:
            branches.append(branch_name)
    return ",".join(branches) if branches else "未知分支"


def get_git_commits_filtered(repo_path: str, target_date_str: str, author: Optional[str] = None) -> list[dict[str, str]]:
    """
    获取指定Git仓库中满足条件的非合并提交信息（从所有分支查询，含分支信息）
    :param repo_path: Git仓库路径（已校验有效性）
    :param target_date_str: 筛选起始日期（YYYY-MM-DD）
    :param author: 提交人名称（None表示所有提交人）
    :return: 提交信息列表（含分支字段）
    """
    query_end_date = datetime.now().strftime("%Y-%m-%d")

    git_cmd = [
        "git",
        "-C", repo_path,
        "log",
        "--no-merges",
        f"--since={target_date_str}",
        f"--until={query_end_date} 23:59:59",
        "--pretty=format:%h|%an|%ad|%s",
        "--date=short",
        "--all"  # 直接从全部分支查询
    ]

    # 添加提交人筛选（指定则过滤）
    if author:
        git_cmd.insert(-1, f"--author={author}")

    result = subprocess.run(
        git_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        check=True
    )

    # 解析提交记录并补充分支信息
    commits = []
    # 用 set 去重（--all 可能导致同一 commit 出现多次）
    seen_hashes = set()
    output_lines = result.stdout.strip().split("\n")
    for line in output_lines:
        if not line:
            continue
        parts = line.split("|")
        if len(parts) >= 4:
            commit_hash = parts[0].strip()
            if commit_hash in seen_hashes:
                continue
            seen_hashes.add(commit_hash)
            # 查询该提交所属分支
            commit_branch = get_commit_branch(repo_path, commit_hash)
            commit_info = {
                "commit_hash": commit_hash,
                "author": parts[1].strip(),
                "commit_date": parts[2].strip(),
                "message": "|".join(parts[3:]).strip(),
                "branch": commit_branch
            }
            commits.append(commit_info)

    return commits


def group_commits_by_date(commits: list[dict[str, str]]) -> list[tuple[str, list[dict[str, str]]]]:
    """将提交记录按日期分组（按日期升序）"""
    date_groups = defaultdict(list)
    for commit in commits:
        date_groups[commit["commit_date"]].append(commit)
    sorted_dates = sorted(date_groups.keys(), reverse=False)
    return [(cm_date, date_groups[cm_date]) for cm_date in sorted_dates]


def format_repo_commits(repo_path: str, commits_list: list[dict[str, str]], date_grouped_commits: list[tuple[str, list[dict[str, str]]]]) -> list[str]:
    """将单个仓库的提交记录格式化为字符串列表"""
    log_line = [f"\n{'=' * 50}", f"仓库：{repo_path}", f"共 {len(commits_list)} 条提交"]

    if commits_list:
        # 汇总该仓库涉及的所有分支和人员（去重、保序）
        all_branches = []
        all_authors = []
        for record in commits_list:
            for br in record["branch"].split(","):
                br = br.strip()
                if br and br not in all_branches:
                    all_branches.append(br)
            if record["author"] not in all_authors:
                all_authors.append(record["author"])
        log_line.append(f"涉及分支：{', '.join(all_branches) if all_branches else '未知'}")
        log_line.append(f"涉及人员：{', '.join(all_authors)}")

    log_line.append(f"{'-' * 25}")

    if not commits_list:
        log_line.append("  📭 无符合条件的提交记录")
    else:
        for commit_date, date_records in date_grouped_commits:
            log_line.append(f"\n【日期：{commit_date}】（共{len(date_records)}条提交）")
            for r_id, record in enumerate(date_records, 1):
                # 每条提交只显示序号和提交信息，不再显示分支和人员
                log_line.append(f"  [{r_id}] {record['message']}")
    return log_line


if __name__ == "__main__":
    today_str = datetime.now().strftime("%Y-%m-%d")

    # ========== 1. 先输入筛选条件：提交人、起始日期 ==========
    print("===== 请先输入筛选条件 =====")

    AUTHOR_NAME = input("请输入要查询的提交人名称（不输入则查询所有提交人）：").strip()
    AUTHOR_NAME = AUTHOR_NAME if AUTHOR_NAME else None

    default_date = get_default_date()
    TARGET_DATE = input(f"请输入筛选的起始日期（格式：YYYY-MM-DD，不输入则默认{default_date}）：").strip()
    TARGET_DATE = TARGET_DATE if TARGET_DATE else default_date

    print(f"\n筛选条件已确认：提交人=[{AUTHOR_NAME if AUTHOR_NAME else '所有'}]，"
          f"日期=[{TARGET_DATE} ~ {today_str}]")

    # ========== 2. 循环询问仓库路径 ==========
    repo_results = []  # 每项：{ "path": str, "commits": [...], "grouped": [...] }
    repo_paths = []  # 记录仓库路径顺序

    print("\n===== 开始输入仓库路径（不输入或输入 0 退出）=====")
    while True:
        input_path = input("\n请输入Git项目路径（不输入或输入0退出）：").strip()
        if not input_path or input_path == "0":
            print("✅ 仓库路径输入完毕，开始查询...")
            break

        abs_path = os.path.abspath(input_path)
        if not is_valid_git_repo(abs_path):
            print(f"❌ {abs_path} 不是有效的Git仓库，请重新输入！")
            continue

        if abs_path in repo_paths:
            print(f"⚠️ 该仓库已添加，跳过重复：{abs_path}")
            continue

        repo_paths.append(abs_path)
        print(f"✅ 已添加：{abs_path}")

    if not repo_paths:
        print("未添加任何仓库，程序结束。")
        exit(0)

    # ========== 3. 查询各仓库的提交记录 ==========
    all_commit_count = 0
    for target_repo in repo_paths:
        print(f"\n🔍 正在查询仓库：{target_repo} ...")
        commit_records = get_git_commits_filtered(target_repo, TARGET_DATE, AUTHOR_NAME)
        date_grouped = group_commits_by_date(commit_records)
        repo_results.append({
            "path": target_repo,
            "commits": commit_records,
            "grouped": date_grouped
        })
        all_commit_count += len(commit_records)
        print(f"   查到 {len(commit_records)} 条提交")

    # ========== 4. 控制台输出 ==========
    print(f"\n{'=' * 50}")
    print(f"===== 筛选条件 =====")
    print(f"提交人：{AUTHOR_NAME if AUTHOR_NAME else '所有提交人'}")
    print(f"日期：{TARGET_DATE} ~ {today_str}")
    print(f"仓库数：{len(repo_paths)}")
    print(f"合计提交：{all_commit_count} 条")
    print(f"{'=' * 50}")

    for rr in repo_results:
        fmt_lines = format_repo_commits(rr["path"], rr["commits"], rr["grouped"])
        for ln in fmt_lines:
            print(ln)

    # ========== 5. 写入文件 ==========
    start_date_format = TARGET_DATE.replace("-", "")
    end_date_format = datetime.now().strftime("%m%d")
    # 用第一个仓库名或多仓库数量作为文件名前缀
    if len(repo_paths) == 1:
        file_prefix = os.path.basename(repo_paths[0])
    else:
        file_prefix = f"多仓库({len(repo_paths)}个)"

    file_name = f"{file_prefix}({start_date_format}-{end_date_format})提交记录_结果.txt"

    # 构建文件内容
    wrt_txt = [
        "===== 筛选条件 =====",
        f"提交人：{AUTHOR_NAME if AUTHOR_NAME else '所有提交人'}",
        f"日期：{TARGET_DATE} ~ {today_str}",
        f"仓库数：{len(repo_paths)}",
        f"合计提交：{all_commit_count} 条",
    ]

    for rr in repo_results:
        fmt_lines = format_repo_commits(rr["path"], rr["commits"], rr["grouped"])
        wrt_txt.extend(fmt_lines)

    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(wrt_txt))
        print(f"\n✅ 提交记录已保存到文件：{os.path.abspath(file_name)}")
    except Exception as e:
        print(f"\n❌ 保存文件失败：{str(e)}")

    # ========== 6. 最后打印日报生成提示词 ==========
    all_commits_flat = []
    for rr in repo_results:
        all_commits_flat.extend(rr["commits"])

    if all_commits_flat:
        # 按日期分组，构建提交摘要供 AI 提示词使用
        grouped_for_prompt = group_commits_by_date(all_commits_flat)
        prompt_lines = []
        for co_date, date_commits in grouped_for_prompt:
            prompt_lines.append(f"【{co_date}】")
            for idx, co_it in enumerate(date_commits, 1):
                prompt_lines.append(f"  {idx}. {co_it['message']}")
        commits_text = "\n".join(prompt_lines)

        print("\n" + "=" * 50)
        print("📋 日报生成提示词（可直接复制给 AI）：")
        print("=" * 50)
        print(
            f"以下是我在 {TARGET_DATE} 至 {today_str} 期间的 Git 提交记录，请根据这些记录帮我撰写每日工作日报。\n"
            f"要求：\n"
            f"1. 按日期分段，每天单独一段；\n"
            f"2. 每条事项用序号列出，语言简洁专业，每条不少于20字；\n"
            f"3. 不要出现仓库名称，只描述实际完成的工作内容；\n"
            f"4. 合并同类项，避免重复罗列。\n\n"
        )
        print("=" * 50)
