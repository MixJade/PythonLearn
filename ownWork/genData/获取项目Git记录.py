# coding=utf-8
# @Time    : 2026/3/21 21:33
# @Software: PyCharm
import os
import subprocess
from collections import defaultdict
from datetime import datetime, timedelta


def is_valid_git_repo(path):
    """校验路径是否为有效的Git仓库（存在.git目录）"""
    if not os.path.exists(path):
        return False
    git_dir = os.path.join(os.path.abspath(path), ".git")
    return os.path.isdir(git_dir)


def get_default_date():
    """获取默认日期：今天的7天前（格式YYYY-MM-DD）"""
    seven_days_ago = datetime.now() - timedelta(days=7)
    return seven_days_ago.strftime("%Y-%m-%d")


def get_all_branches(repo_path):
    """获取仓库所有本地分支名称"""
    result = subprocess.run(
        ["git", "-C", repo_path, "branch", "--list"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        check=True
    )
    branches = []
    for line in result.stdout.strip().split("\n"):
        branch_name = line.strip().replace("*", "").strip()
        if branch_name:
            branches.append(branch_name)
    return branches


def get_commit_branch(repo_path, commit_hash):
    """获取单个提交所属的分支（优先本地分支，多个分支用逗号分隔）"""
    # git branch --contains 查找包含该提交的所有分支
    result = subprocess.run(
        ["git", "-C", repo_path, "branch", "--contains", commit_hash],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        check=True
    )
    branches = []
    for line in result.stdout.strip().split("\n"):
        branch_name = line.strip().replace("*", "").strip()
        if branch_name and branch_name not in branches:
            branches.append(branch_name)
    # 无匹配分支则显示「未知分支」
    return ",".join(branches) if branches else "未知分支"


def get_git_commits_filtered(repo_path, target_date_str, branch=None, author=None):
    """
    不依赖第三方库，获取指定Git仓库中满足条件的非合并提交信息（含分支信息）
    :param repo_path: Git仓库路径（已校验有效性）
    :param target_date_str: 筛选起始日期（YYYY-MM-DD）
    :param branch: 分支名称（None表示所有分支）
    :param author: 提交人名称（None表示所有提交人）
    :return: 提交信息列表（含分支字段）
    """
    # 构造基础git log命令（仅获取核心提交信息，分支单独查询）
    git_cmd = [
        "git",
        "-C", repo_path,
        "log",
        "--no-merges",
        f"--since={target_date_str}",
        "--pretty=format:%h|%an|%ad|%s",
        "--date=short"
    ]

    # 添加提交人筛选（指定则过滤）
    if author:
        git_cmd.insert(-1, f"--author={author}")

    # 添加分支筛选（None则查所有分支，否则查指定分支）
    if branch:
        git_cmd.append(branch)
    else:
        git_cmd.append("--all")  # 所有分支/标签等引用

    result = subprocess.run(
        git_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        check=True
    )

    # 解析提交记录并补充分支信息
    commits = []
    output_lines = result.stdout.strip().split("\n")
    for line in output_lines:
        if not line:
            continue
        parts = line.split("|")
        if len(parts) >= 4:
            commit_hash = parts[0].strip()
            # 查询该提交所属分支
            commit_branch = get_commit_branch(repo_path, commit_hash)
            commit_info = {
                "commit_hash": commit_hash,
                "author": parts[1].strip(),
                "commit_date": parts[2].strip(),
                "message": "|".join(parts[3:]).strip(),
                "branch": commit_branch  # 新增分支字段
            }
            commits.append(commit_info)

    return commits


def group_commits_by_date(commits):
    """将提交记录按日期分组"""
    date_groups = defaultdict(list)
    for commit in commits:
        date_groups[commit["commit_date"]].append(commit)
    # 按日期倒序排列分组（最新日期在后）
    sorted_dates = sorted(date_groups.keys(), reverse=False)
    return [(cm_date, date_groups[cm_date]) for cm_date in sorted_dates]


if __name__ == "__main__":
    # 1. 循环获取有效的Git仓库路径
    REPO_PATH = ""
    while True:
        input_path = input("请输入Git项目路径（不输入则使用当前目录）：").strip()
        # 处理空输入（默认当前目录）
        REPO_PATH = input_path if input_path else "./"
        # 校验路径有效性
        if is_valid_git_repo(REPO_PATH):
            REPO_PATH = os.path.abspath(REPO_PATH)  # 转为绝对路径，提升可读性
            print(f"✅ 验证通过：{REPO_PATH} 是有效的Git仓库")
            break
        else:
            print(f"❌ 错误：{os.path.abspath(REPO_PATH)} 不是有效的Git仓库，请重新输入！")

    # 2. 获取日期输入（默认7天前）
    default_date = get_default_date()
    TARGET_DATE = input(f"请输入筛选的起始日期（格式：YYYY-MM-DD，不输入则默认{default_date}）：").strip()
    TARGET_DATE = TARGET_DATE if TARGET_DATE else default_date

    # 3. 获取分支输入（提示所有分支）
    all_branches = get_all_branches(REPO_PATH)
    print(f"\n当前仓库的本地分支列表：{all_branches if all_branches else '无'}")
    BRANCH_NAME = input("请输入要查询的分支名称（不输入则查询所有分支）：").strip()
    BRANCH_NAME = BRANCH_NAME if BRANCH_NAME else None

    # 4. 获取提交人输入
    AUTHOR_NAME = input("请输入要查询的提交人名称（不输入则查询所有提交人）：").strip()
    AUTHOR_NAME = AUTHOR_NAME if AUTHOR_NAME else None

    # 5. 获取并分组提交信息
    print("\n🔍 正在查询符合条件的提交记录（含分支信息）...")
    commits_list = get_git_commits_filtered(REPO_PATH, TARGET_DATE, BRANCH_NAME, AUTHOR_NAME)
    date_grouped_commits = group_commits_by_date(commits_list)

    # 6. 格式化输出结果（按日期分组展示，含分支信息）
    print(f"\n===== 筛选条件 =====")
    print(f"Git仓库：{REPO_PATH}")
    print(f"日期：{TARGET_DATE} 及以后（默认7天前）")
    print(f"分支：{BRANCH_NAME if BRANCH_NAME else '所有分支'}")
    print(f"提交人：{AUTHOR_NAME if AUTHOR_NAME else '所有提交人'}")
    print(f"\n===== 共 {len(commits_list)} 条 =====")

    if not commits_list:
        print("📭 无符合条件的提交记录")
    else:
        version_idx = 1
        for date, date_commits in date_grouped_commits:
            print(f"\n【日期：{date}】（共{len(date_commits)}条提交）")
            for idx, co_it in enumerate(date_commits, 1):
                print(
                    f"  [{idx}] [{co_it['branch']}]【{co_it['author']}】：{co_it['message']}")
            version_idx += 1

    # 7. 将结果保存到TXT文件
    start_date_format = TARGET_DATE.replace("-", "")
    end_date_format = datetime.now().strftime("%m%d")
    folder_name = os.path.basename(REPO_PATH)
    file_name = f"{folder_name}({start_date_format}-{end_date_format})提交记录_结果.txt"
    # 拼接要写入的内容
    wrt_txt = ["===== 筛选条件 =====", f"Git仓库：{REPO_PATH}", f"日期：{TARGET_DATE} 及以后（默认7天前）",
               f"分支：{BRANCH_NAME if BRANCH_NAME else '所有分支'}",
               f"提交人：{AUTHOR_NAME if AUTHOR_NAME else '所有提交人'}",
               f"\n===== 共 {len(commits_list)} 条 =====\n"]

    if not commits_list:
        wrt_txt.append("📭 无符合条件的提交记录")
    else:
        for co_date, date_commits in date_grouped_commits:
            wrt_txt.append(f"\n【日期：{co_date}】（共{len(date_commits)}条提交）")
            for idx, co_it in enumerate(date_commits, 1):
                wrt_txt.append(f"  [{idx}] {co_it['message']}")

    # 写入文件（编码为utf-8，避免中文乱码）
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(wrt_txt))
        print(f"\n✅ 提交记录已保存到文件：{os.path.abspath(file_name)}")
        print("根据这些Git提交记录，按照1234的序号为每天写日报(不要带具体仓库名称，只整理每天的事项)，每一项至少20字")
    except Exception as e:
        print(f"\n❌ 保存文件失败：{str(e)}")
