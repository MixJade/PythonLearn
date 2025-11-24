# coding=utf-8
# @Time    : 2025/11/24 20:32
# @Software: PyCharm
import json
import re
import subprocess
import sys


def get_installed_packages():
    """使用pip list命令获取当前环境已安装的包，排除pip/setuptools/wheel"""
    installed = {}
    ignore_pkgs = {"pip", "setuptools", "wheel"}
    # 运行 pipdeptree 命令获取 JSON 格式的输出
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=json"],
        capture_output=True, text=True, check=True
    )

    # 解析 JSON 输出
    packages = json.loads(result.stdout)
    for pkg in packages:
        name = pkg["name"]  # 使用 pipdeptree 提供的规范化包名
        if name not in ignore_pkgs:
            installed[name] = pkg["version"]
    return installed


def parse_requirements_file(file_path):
    """
    解析requirements.txt（兼容注释、git依赖、环境标记、URL等）
    返回：{包名: 版本}（版本为None表示无法提取精确版本）
    """
    reqs = {}
    # 匹配包名的基础正则（兼容大多数格式）
    pkg_name_pattern = re.compile(r'^([a-zA-Z0-9_\-]+)', re.IGNORECASE)
    # 匹配==精确版本的正则
    version_pattern = re.compile(r'==\s*([0-9a-zA-Z_\\.+-]+)')

    with open(file_path, "r", encoding="utf-16") as f:
        for line_num, line in enumerate(f, 1):
            # 清理行内容：移除注释、环境标记、换行符
            line_clean = line.strip()
            if not line_clean or line_clean.startswith("#"):
                continue

            # 移除环境标记（如 ; python_version >= "3.8"）
            line_clean = re.split(r';\s*', line_clean)[0].strip()
            # 移除git/URL部分（如 git+https://xxx#egg=package 或 https://xxx.whl）
            line_clean = re.sub(r'git\+.*#egg=|https?://.*', '', line_clean).strip()
            if not line_clean:
                continue

            # 提取包名
            pkg_name_match = pkg_name_pattern.match(line_clean)
            if not pkg_name_match:
                print(f"警告：第{line_num}行无法解析包名，跳过: {line.strip()}")
                continue
            pkg_name = pkg_name_match.group(1)

            # 提取精确版本（仅==）
            version_match = version_pattern.search(line_clean)
            pkg_version = version_match.group(1) if version_match else None

            reqs[pkg_name] = pkg_version
    return reqs


def sync_requirements(req_file):
    # 1. 获取已安装包和目标包
    installed = get_installed_packages()
    target = parse_requirements_file(req_file)
    target_names = set(target.keys())
    installed_names = set(installed.keys())
    print(f"已安装包数量：{len(installed_names)}")
    print(f"require包数量：{len(target_names)}")
    # 2. 找出需要卸载的包（已安装但不在目标清单中）
    to_uninstall = installed_names - target_names
    # 3. 找出需要安装/更新的包（目标清单中但未安装，或版本不匹配）
    to_install = []
    for name, target_ver in target.items():
        if name not in installed:
            to_install.append(name if target_ver is None else f"{name}=={target_ver}")
        else:
            installed_ver = installed[name]
            if target_ver and installed_ver != target_ver:
                to_install.append(f"{name}=={target_ver}")

    # 4. 执行卸载
    if to_uninstall:
        cmd = [sys.executable, "-m", "pip", "uninstall", "-y"] + list(to_uninstall)
        print("\n=== 下列包需要卸载 ===")
        print(" ".join(cmd))
    else:
        print("\n=== 无多余包需要卸载 ===")

    # 5. 执行安装/更新
    if to_install:
        cmd = [sys.executable, "-m", "pip", "install"] + to_install
        print("\n=== 下列包需要安装 ===")
        print(" ".join(cmd))
    else:
        print("\n=== 无缺失包需要安装/更新 ===")

    # 6. 最终校验
    print("\n=== 最终校验 ===")
    final_installed = get_installed_packages()
    mismatch = []
    for name, target_ver in target.items():
        if name not in final_installed:
            mismatch.append(f"{name}: 未安装（目标要求: {target_ver or '任意版本'}）")
        elif target_ver and final_installed[name] != target_ver:
            mismatch.append(f"{name}: 版本不匹配（已安装: {final_installed[name]}, 目标: {target_ver}）")

    if mismatch:
        print("❌ 存在不匹配项:")
        for m in mismatch:
            print(f"  - {m}")
        sys.exit(1)
    else:
        print("✅ 所有依赖已完全匹配requirements.txt")


if __name__ == "__main__":
    sync_requirements("requirements.txt")
