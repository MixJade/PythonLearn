# coding=utf-8
# @Time    : 2026/3/21 21:33
# @Software: PyCharm
# @Description: Git提交记录查询工具 - 命令行版本
import os
import subprocess
import argparse
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


def run_git_query(author: Optional[str], start_date: str, repo_paths: list[str]) -> dict:
    """执行Git查询的主函数"""
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

    return {
        "author": author,
        "start_date": start_date,
        "end_date": today_str,
        "repo_count": len(repo_paths),
        "total_commits": all_commit_count,
        "repo_results": repo_results,
        "output_text": "\n".join(wrt_txt)
    }


def save_to_file(output_text: str, start_date: str, repo_paths: list[str]) -> str:
    """保存结果到桌面文件"""
    start_date_format = start_date.replace("-", "")
    end_date_format = datetime.now().strftime("%m%d")

    if len(repo_paths) == 1:
        file_prefix_str = os.path.basename(repo_paths[0])
    else:
        file_prefix_str = f"多仓库({len(repo_paths)}个)"

    file_name = f"{file_prefix_str}({start_date_format}-{end_date_format})提交记录_结果.txt"

    dir_name = "日报" + datetime.now().strftime("%Y%m%d")
    out_dir = os.path.join(os.path.expanduser("~"), "Desktop", dir_name)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    outfile_path = os.path.join(out_dir, file_name)
    with open(outfile_path, "w", encoding="utf-8") as f:
        f.write(output_text)

    return os.path.abspath(outfile_path)


def main():
    parser = argparse.ArgumentParser(
        description="Git提交记录查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python GetPrjGitRecords.py --author 张三 --start-date 2026-07-01 --repos "D:\\proj\\ui" "D:\\proj\\api"
  python GetPrjGitRecords.py --start-date 2026-07-01 --repos "D:\\proj\\ui"
  python GetPrjGitRecords.py --repos "D:\\proj\\ui" "D:\\proj\\api"
        """
    )

    parser.add_argument(
        "-a", "--author",
        type=str,
        default=None,
        help="提交人名称（不指定则查询所有提交人）"
    )

    parser.add_argument(
        "-s", "--start-date",
        type=str,
        default=None,
        help=f"起始日期（格式：YYYY-MM-DD，不指定则默认7天前，即 {get_default_date()}）"
    )

    parser.add_argument(
        "-r", "--repos",
        type=str,
        nargs="+",
        required=True,
        help="Git仓库路径列表（至少一个路径）"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="输出文件路径（不指定则保存到桌面）"
    )

    args = parser.parse_args()

    start_date = args.start_date if args.start_date else get_default_date()

    print(f"===== Git提交记录查询 =====")
    print(f"提交人：{args.author if args.author else '所有'}")
    print(f"起始日期：{start_date}")
    print(f"仓库数量：{len(args.repos)}")
    for repo in args.repos:
        print(f"  - {repo}")
    print("=" * 40)

    result = run_git_query(args.author, start_date, args.repos)

    print(result["output_text"])

    if args.output:
        outfile_path = args.output
        with open(outfile_path, "w", encoding="utf-8") as f:
            f.write(result["output_text"])
        print(f"\n✅ 已保存到：{os.path.abspath(outfile_path)}")
    else:
        outfile_path = save_to_file(result["output_text"], start_date, args.repos)
        print(f"\n✅ 已保存到：{outfile_path}")

    print(f"\n===== 统计 =====")
    print(f"合计提交：{result['total_commits']} 条")
    print(f"涉及仓库：{result['repo_count']} 个")


if __name__ == "__main__":
    main()
