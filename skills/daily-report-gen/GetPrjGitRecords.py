# coding=utf-8
# @Time    : 2026/3/21 21:33
# @Software: PyCharm
import os
import sys
import json
import argparse
import subprocess
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional

# 无参数运行时打印的提示（固定文案）
USAGE_HINT = r"""用法：
  python GetPrjGitRecords.py -a <配置文件> -b <模块名> [-s <起始日期>]

参数：
  -a, --config      配置文件路径（JSON），必填
  -b, --module      模块名，对应配置里 projects 的键，必填
  -s, --start-date  起始日期 YYYY-MM-DD（不填则默认近 7 天；传 _ 则交互输入）

示例：
  python GetPrjGitRecords.py -a example\样例配置.json -b 项目管理
  python GetPrjGitRecords.py -a example\样例配置.json -b 项目管理 -s 2026-07-01
  python GetPrjGitRecords.py -a example\样例配置.json -b 项目管理 -s _

请先参照脚本所在目录下 example 目录中的 样例配置.json 和 样例.cmd 完成配置。"""


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


def prompt_start_date() -> str:
    """交互输入起始日期（直接回车使用默认的7天前）"""
    default_date = get_default_date()
    tip = f"请输入起始日期（YYYY-MM-DD），直接回车使用默认值：{default_date}\n> "

    while True:
        try:
            user_input = input(tip).strip()
        except EOFError:
            return default_date

        if not user_input:
            return default_date

        try:
            datetime.strptime(user_input, "%Y-%m-%d")
            return user_input
        except ValueError:
            print("日期格式不对，请按 YYYY-MM-DD 输入，例如 2026-10-30")


# ---------------------------------------------------------------- 配置相关

def load_config(config_path: str) -> dict:
    """读取JSON配置文件，并校验基本结构"""
    abs_path = os.path.abspath(config_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"配置文件不存在：{abs_path}")

    with open(abs_path, "r", encoding="utf-8-sig") as f:
        config = json.load(f)

    return config


def resolve_module(config: dict, module_name: str) -> tuple[str, list[str]]:
    """根据模块名取出 (模块名, 仓库路径列表)，匹配不到时列出可用模块"""
    projects = config["projects"]

    if module_name in projects:
        return module_name, list(projects[module_name]["paths"])

    for name, conf in projects.items():
        if name.strip().lower() == module_name.strip().lower():
            return name, list(conf["paths"])

    available = "、".join(projects.keys())
    raise KeyError(f"配置文件中找不到模块 [{module_name}]，可用模块：{available}")


# ---------------------------------------------------------------- Git 查询

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
        if branch_name and "->" not in branch_name and branch_name not in branches:
            branches.append(branch_name)
    return ",".join(branches) if branches else "未知分支"


def get_git_commits_filter(repo_path: str, target_date_str: str, author: Optional[str] = None) -> list[dict[str, str]]:
    """获取指定Git仓库中满足条件的非合并提交信息（从所有分支查询，含分支信息）"""
    query_end_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    git_cmd = [
        "git",
        "-C", repo_path,
        "log",
        "--no-merges",
        f"--since={target_date_str} 00:00:00",
        f"--until={query_end_date} 00:00:00",
        "--pretty=format:%h|%an|%ad|%s",
        "--date=short",
        "--all"
    ]

    if author:
        git_cmd.insert(-1, f"--author={author}")

    result = subprocess.run(
        git_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        check=True
    )

    commits = []
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


def format_repo_commits(repo_path: str, commits_list: list[dict[str, str]],
                        date_grouped_commits: list[tuple[str, list[dict[str, str]]]]) -> list[str]:
    """将单个仓库的提交记录格式化为字符串列表"""
    log_line = [f"\n{'=' * 50}", f"仓库：{repo_path}", f"共 {len(commits_list)} 条提交"]

    if commits_list:
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
        log_line.append("  [无符合条件的提交记录]")
    else:
        for commit_date, date_records in date_grouped_commits:
            log_line.append(f"\n【日期：{commit_date}】（共{len(date_records)}条提交）")
            for r_id, record in enumerate(date_records, 1):
                log_line.append(f"  [{r_id}] {record['message']}")
    return log_line


def run_git_query(author: Optional[str], start_date: str, repo_paths: list[str]) -> tuple[str, int]:
    """执行Git查询，返回 (提交记录文本, 提交条数)"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    repo_results = []
    all_commit_count = 0

    for target_repo in repo_paths:
        abs_path = os.path.abspath(target_repo)
        if not is_valid_git_repo(abs_path):
            print(f"[跳过无效仓库] {abs_path}")
            continue

        commit_records = get_git_commits_filter(abs_path, start_date, author)
        date_grouped = group_commits_by_date(commit_records)
        repo_results.append({
            "path": abs_path,
            "commits": commit_records,
            "grouped": date_grouped
        })
        all_commit_count += len(commit_records)

    wrt_txt = [
        "===== 筛选条件 =====",
        f"提交人：{author if author else '所有提交人'}",
        f"日期：{start_date} ~ {today_str}",
        f"仓库数：{len(repo_paths)}",
        f"合计提交：{all_commit_count} 条",
    ]

    for rr in repo_results:
        fmt_lines = format_repo_commits(rr["path"], rr["commits"], rr["grouped"])
        wrt_txt.extend(fmt_lines)

    return "\n".join(wrt_txt), all_commit_count


def save_to_file(output_text: str, file_name: str) -> str:
    """保存结果到桌面 日报YYYYMMDD 文件夹"""
    dir_name = "日报" + datetime.now().strftime("%Y%m%d")
    out_dir = os.path.join(os.path.expanduser("~"), "Desktop", dir_name)
    os.makedirs(out_dir, exist_ok=True)

    outfile_path = os.path.join(out_dir, file_name)
    with open(outfile_path, "w", encoding="utf-8") as f:
        f.write(output_text)

    return os.path.abspath(outfile_path)


def main():
    parser = argparse.ArgumentParser(
        description="Git提交记录查询工具（配置文件 + 模块名）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=r"""
示例:
  python GetPrjGitRecords.py -a example\样例配置.json -b 项目管理
  python GetPrjGitRecords.py -a example\样例配置.json -b 项目管理 -s 2026-07-01
  python GetPrjGitRecords.py -a example\样例配置.json -b 项目管理 -s _    # 交互输入日期
        """
    )

    parser.add_argument(
        "-a", "--config",
        type=str,
        default=None,
        help=r"配置文件路径（JSON），格式参考 example 目录下的样例配置.json"
    )

    parser.add_argument(
        "-b", "--module",
        type=str,
        default=None,
        help="模块名，即 JSON 中 projects 下的键，必填"
    )

    parser.add_argument(
        "-s", "--start-date",
        type=str,
        default=None,
        help=f"起始日期（YYYY-MM-DD），不指定则默认7天前（{get_default_date()}）；传 _ 则交互输入"
    )

    # 无参数运行：只打印用法提示
    if len(sys.argv) <= 1:
        print(USAGE_HINT)
        return

    args = parser.parse_args()

    if not args.config:
        parser.error(r"缺少配置文件参数，请使用 -a 指定JSON配置文件，例如：-a example\样例配置.json")

    if not args.module:
        parser.error(r"必须指定模块名，请用 -b 指定，例如：-b 项目管理")

    # 读取并校验配置
    try:
        config = load_config(args.config)
    except FileNotFoundError as e:
        print(f"[错误] {e}")
        sys.exit(1)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"[错误] 配置文件解析失败：{e}")
        sys.exit(1)

    try:
        module_name, repo_paths = resolve_module(config, args.module)
    except KeyError as e:
        print(f"[错误] {e.args[0]}")
        sys.exit(1)

    author = config.get("author_name")

    if args.start_date == "_":
        start_date = prompt_start_date()
    elif args.start_date:
        start_date = args.start_date
    else:
        start_date = get_default_date()

    print("===== Git提交记录查询 =====")
    print(f"配置文件：{os.path.abspath(args.config)}")
    print(f"提交人：{author if author else '所有'}")
    print(f"起始日期：{start_date}")
    print(f"模块：{module_name}（{len(repo_paths)} 个仓库）")
    for one_repo in repo_paths:
        print(f"      {one_repo}")
    print("=" * 40)

    output_text, commit_count = run_git_query(author, start_date, repo_paths)
    print(output_text)

    start_format = start_date.replace("-", "")
    end_format = datetime.now().strftime("%m%d")
    file_name = f"{module_name}({start_format}-{end_format})提交记录_结果.txt"

    saved = save_to_file(output_text, file_name)

    print(f"\n[已保存] {saved}")
    print("\n===== 统计 =====")
    print(f"合计提交：{commit_count} 条")


if __name__ == "__main__":
    main()
