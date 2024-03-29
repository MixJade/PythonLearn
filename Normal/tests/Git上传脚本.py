# coding=utf-8
# @Time    : 2024/3/8 15:15
# @Software: PyCharm
import subprocess

# 定义提交消息
commit_message = "MixJade"

# 添加所有文件(这只会添加当前文件夹的文件)
subprocess.run(["git", "add", "."])

# 提交所有更改
subprocess.run(["git", "commit", "-m", commit_message])

# 推送到远程仓库
subprocess.run(["git", "push", "origin", "main"])
